#include <assert.h>
#include <stdint.h>
#include <string.h>
#include "common.h"

s32 func_80007024_7C24(s32);

enum {
    SCHEDULER_QUEUE_OFFSET = 0x40,
    SCHEDULER_NOTIFY_OFFSET = 0x20,
    SCHEDULER_LIST_HEAD_OFFSET = 0x298,
    SCHEDULER_MESSAGE_29A = 0x29A,
    SCHEDULER_MESSAGE_29B = 0x29B,
    SCHEDULER_MESSAGE_29C = 0x29C,
    SCHEDULER_MESSAGE_29D = 0x29D,
    SCHEDULER_FUNC_07204 = 0x80007204u,
    SCHEDULER_FUNC_07324 = 0x80007324u,
    SCHEDULER_FUNC_07478 = 0x80007478u,
    SCHEDULER_FUNC_07160 = 0x80007160u,
    SCHEDULER_TRACE_CAPACITY = 32
};

/* Raw MIPS fields: next pointer at +0 and destination OSMesgQueue* at +4. */
typedef struct SchedulerQueueNode {
    struct SchedulerQueueNode *next;
    uint32_t queue_address;
} SchedulerQueueNode;

typedef enum {
    SCHEDULER_TRACE_BLOCKING_RECEIVE,
    SCHEDULER_TRACE_RECEIVE,
    SCHEDULER_TRACE_CALLBACK,
    SCHEDULER_TRACE_DEFAULT_HANDLER,
    SCHEDULER_TRACE_SEND
} SchedulerTraceKind;

typedef struct {
    SchedulerTraceKind kind;
    uint32_t arg0; /* queue or callback address */
    uint32_t arg1; /* first traced argument, queue message, or owner */
    uint32_t arg2; /* flags, received message, or second callback argument */
} SchedulerTraceEvent;

typedef struct SchedulerQueueReference SchedulerQueueReference;
typedef void (*SchedulerEventHook)(void *, SchedulerQueueReference *, uint32_t);
typedef void (*SchedulerSendHook)(void *, SchedulerQueueReference *,
                                  SchedulerQueueNode *, uint32_t);

struct SchedulerQueueReference {
    uint32_t owner_address;
    SchedulerQueueNode *list_head;
    SchedulerTraceEvent trace[SCHEDULER_TRACE_CAPACITY];
    uint32_t trace_count;
    SchedulerEventHook event_hook;
    void *event_hook_context;
    SchedulerSendHook send_hook;
    void *send_hook_context;
};

/* MIPS addiu uses 32-bit guest-address arithmetic; model it without host pointers. */
static uint32_t scheduler_guest_add(uint32_t base, uint32_t offset) {
    return base + offset;
}

static void scheduler_trace(SchedulerQueueReference *state,
                            SchedulerTraceKind kind,
                            uint32_t arg0,
                            uint32_t arg1,
                            uint32_t arg2) {
    SchedulerTraceEvent *event;

    assert(state->trace_count < SCHEDULER_TRACE_CAPACITY);
    event = &state->trace[state->trace_count++];
    event->kind = kind;
    event->arg0 = arg0;
    event->arg1 = arg1;
    event->arg2 = arg2;
}

/* One completed receive/dispatch step from the original worker loop. */
static void scheduler_dispatch_reference(SchedulerQueueReference *state,
                                         uint32_t message) {
    uint32_t callback;

    switch (message) {
    case SCHEDULER_MESSAGE_29A:
        callback = SCHEDULER_FUNC_07204;
        break;
    case SCHEDULER_MESSAGE_29B:
        callback = SCHEDULER_FUNC_07324;
        break;
    case SCHEDULER_MESSAGE_29C:
        callback = SCHEDULER_FUNC_07478;
        break;
    case SCHEDULER_MESSAGE_29D: {
        SchedulerQueueNode *node = state->list_head;

        while (node != 0) {
            uint32_t destination_queue = node->queue_address;

            /* Original call: osSendMesg(node->queue, owner + 0x20, 0). */
            scheduler_trace(state, SCHEDULER_TRACE_SEND,
                            destination_queue,
                            scheduler_guest_add(state->owner_address,
                                                SCHEDULER_NOTIFY_OFFSET), 0);
            if (state->send_hook != 0) {
                state->send_hook(state->send_hook_context, state, node,
                                 destination_queue);
            }

            /* MIPS reloads node->next after osSendMesg returns. */
            node = node->next;
        }
        return;
    }
    default:
        /* Trace 07160's actual call tuple: a0=owner, a1=received message. */
        scheduler_trace(state, SCHEDULER_TRACE_DEFAULT_HANDLER,
                        SCHEDULER_FUNC_07160, state->owner_address, message);
        if (state->event_hook != 0) {
            state->event_hook(state->event_hook_context, state, message);
        }
        return;
    }

    scheduler_trace(state, SCHEDULER_TRACE_CALLBACK, callback,
                    state->owner_address, message);
    if (state->event_hook != 0) {
        state->event_hook(state->event_hook_context, state, message);
    }
}

/* A finite test harness for completed receives; count zero means receive blocks. */
static void scheduler_run_reference(SchedulerQueueReference *state,
                                    const uint32_t *messages,
                                    uint32_t message_count) {
    uint32_t queue_address;
    uint32_t i;

    queue_address = scheduler_guest_add(state->owner_address,
                                        SCHEDULER_QUEUE_OFFSET);
    if (message_count == 0) {
        scheduler_trace(state, SCHEDULER_TRACE_BLOCKING_RECEIVE,
                        queue_address, 1, 0);
        return;
    }

    for (i = 0; i < message_count; i++) {
        scheduler_trace(state, SCHEDULER_TRACE_RECEIVE,
                        queue_address, 1, messages[i]);
        scheduler_dispatch_reference(state, messages[i]);
    }
}

static void scheduler_init(SchedulerQueueReference *state,
                           uint32_t owner_address) {
    memset(state, 0, sizeof(*state));
    state->owner_address = owner_address;
}

static void replace_list_head_after_callback(void *context,
                                             SchedulerQueueReference *state,
                                             uint32_t message) {
    /* Injected mutation for reload coverage; this is not a claim about 29A effects. */
    if (message == SCHEDULER_MESSAGE_29A) {
        state->list_head = (SchedulerQueueNode *)context;
    }
}

typedef struct {
    SchedulerQueueNode *redirect;
    uint32_t replacement_queue;
    uint32_t fired;
} SchedulerSendMutation;

static void mutate_live_list_during_send(void *context,
                                         SchedulerQueueReference *state,
                                         SchedulerQueueNode *node,
                                         uint32_t message) {
    SchedulerSendMutation *mutation = (SchedulerSendMutation *)context;

    /* Injected scheduling-boundary mutation; not a claim that osSendMesg does this. */
    (void)state;
    (void)message;
    if (!mutation->fired) {
        node->next = mutation->redirect;
        mutation->redirect->queue_address = mutation->replacement_queue;
        mutation->fired = 1;
    }
}

static void test_pointer_offsets_use_32_bit_guest_arithmetic(void) {
    assert(func_80007024_7C24(0) == SCHEDULER_QUEUE_OFFSET);
    assert(func_80007024_7C24(0x1000) == 0x1040);
    assert(func_80007024_7C24(-0x40) == 0);

    assert(scheduler_guest_add(0x80010000u, SCHEDULER_QUEUE_OFFSET) ==
           0x80010040u);
    assert(scheduler_guest_add(0x80010000u, SCHEDULER_NOTIFY_OFFSET) ==
           0x80010020u);
    assert(scheduler_guest_add(0x80010000u, SCHEDULER_LIST_HEAD_OFFSET) ==
           0x80010298u);
    assert(scheduler_guest_add(0xFFFFFFC0u, SCHEDULER_QUEUE_OFFSET) == 0);
}

static void test_empty_queue_waits_without_dispatch(void) {
    SchedulerQueueReference state;

    scheduler_init(&state, 0x80010000u);
    scheduler_run_reference(&state, 0, 0);

    assert(state.trace_count == 1);
    assert(state.trace[0].kind == SCHEDULER_TRACE_BLOCKING_RECEIVE);
    assert(state.trace[0].arg0 == 0x80010040u);
    assert(state.trace[0].arg1 == 1);
}

static void test_single_and_multiple_message_dispatch_order(void) {
    SchedulerQueueReference single;
    SchedulerQueueReference multiple;
    const uint32_t one[] = {SCHEDULER_MESSAGE_29A};
    const uint32_t many[] = {
        SCHEDULER_MESSAGE_29B,
        SCHEDULER_MESSAGE_29C,
        0x80300024u,
    };

    scheduler_init(&single, 0x80020000u);
    scheduler_run_reference(&single, one, 1);
    assert(single.trace_count == 2);
    assert(single.trace[0].kind == SCHEDULER_TRACE_RECEIVE);
    assert(single.trace[0].arg0 == 0x80020040u && single.trace[0].arg1 == 1);
    assert(single.trace[1].kind == SCHEDULER_TRACE_CALLBACK);
    assert(single.trace[1].arg0 == SCHEDULER_FUNC_07204);
    assert(single.trace[1].arg1 == 0x80020000u);

    scheduler_init(&multiple, 0x80030000u);
    scheduler_run_reference(&multiple, many, 3);
    assert(multiple.trace_count == 6);
    assert(multiple.trace[0].kind == SCHEDULER_TRACE_RECEIVE);
    assert(multiple.trace[1].kind == SCHEDULER_TRACE_CALLBACK);
    assert(multiple.trace[1].arg0 == SCHEDULER_FUNC_07324);
    assert(multiple.trace[2].kind == SCHEDULER_TRACE_RECEIVE);
    assert(multiple.trace[3].kind == SCHEDULER_TRACE_CALLBACK);
    assert(multiple.trace[3].arg0 == SCHEDULER_FUNC_07478);
    assert(multiple.trace[4].kind == SCHEDULER_TRACE_RECEIVE);
    assert(multiple.trace[5].kind == SCHEDULER_TRACE_DEFAULT_HANDLER);
    assert(multiple.trace[5].arg0 == SCHEDULER_FUNC_07160);
    assert(multiple.trace[5].arg1 == 0x80030000u);
    assert(multiple.trace[5].arg2 == 0x80300024u);
}

enum {
    SCHEDULER_FUNC_07634 = 0x80007634u,
    SCHEDULER_FUNC_077B8 = 0x800077B8u,
    SCHEDULER_FUNC_0769C = 0x8000769Cu,
    SCHEDULER_EVENT_CALL_CAPACITY = 3
};

typedef struct {
    uint32_t function;
    uint32_t a0;
    uint32_t a1;
    uint32_t a2;
    uint32_t a3;
} SchedulerEventCall;

typedef struct {
    uint32_t guest_address;
    uint32_t count_2b4;
    uint32_t state_2ac;
    uint32_t state_2b0;
} SchedulerEventOwner;

/* Helpers are recorded/mocked; these controls do not assert their native effects. */
typedef struct {
    SchedulerEventOwner owner;
    uint32_t last_message;
    uint8_t global_gate_byte;
    uint32_t check_result;
    uint32_t check_output_1;
    uint32_t check_output_2;
    uint32_t frame_sp;
    uint32_t prepare_seen_count;
    uint32_t prepare_seen_message;
    SchedulerEventCall calls[SCHEDULER_EVENT_CALL_CAPACITY];
    uint32_t call_count;
} SchedulerEventReference;

static void scheduler_record_event_call(SchedulerEventReference *state,
                                        uint32_t function,
                                        uint32_t a0,
                                        uint32_t a1,
                                        uint32_t a2,
                                        uint32_t a3) {
    SchedulerEventCall *call;

    assert(state->call_count < SCHEDULER_EVENT_CALL_CAPACITY);
    call = &state->calls[state->call_count++];
    call->function = function;
    call->a0 = a0;
    call->a1 = a1;
    call->a2 = a2;
    call->a3 = a3;
}

/* One default-message path from 07160; outputs/return are the 077B8 mock. */
static void scheduler_default_message_reference(SchedulerEventReference *state,
                                                uint32_t message) {
    uint32_t flags;

    state->owner.count_2b4++;
    if (message == state->last_message) {
        return;
    }
    state->last_message = message;

    scheduler_record_event_call(state, SCHEDULER_FUNC_07634,
                                state->owner.guest_address, message, 0, 0);
    state->prepare_seen_count = state->owner.count_2b4;
    state->prepare_seen_message = state->last_message;

    /* MIPS tests bit 1 when +0x2AC is zero and bit 0 when +0x2B0 is zero. */
    flags = (state->owner.state_2ac == 0 ? 2u : 0u) |
            (state->owner.state_2b0 == 0 ? 1u : 0u);
    scheduler_record_event_call(state, SCHEDULER_FUNC_077B8,
                                state->owner.guest_address,
                                scheduler_guest_add(state->frame_sp, 0x24),
                                scheduler_guest_add(state->frame_sp, 0x20),
                                flags);

    if (state->check_result == flags || state->global_gate_byte != 0) {
        return;
    }

    scheduler_record_event_call(state, SCHEDULER_FUNC_0769C,
                                state->owner.guest_address,
                                state->check_output_1,
                                state->check_output_2, 0);
}

static void scheduler_event_reference_init(SchedulerEventReference *state,
                                           uint32_t owner_address) {
    memset(state, 0, sizeof(*state));
    state->owner.guest_address = owner_address;
    state->frame_sp = 0x7FFFE000u;
}

static void test_default_message_duplicate_still_increments_word_counter(void) {
    SchedulerEventReference state;
    const uint32_t message = 0;

    scheduler_event_reference_init(&state, 0x80080000u);
    state.owner.count_2b4 = 0xFFFFFFFFu;
    state.last_message = message;
    scheduler_default_message_reference(&state, message);

    assert(state.owner.count_2b4 == 0);
    assert(state.last_message == message);
    assert(state.call_count == 0);
}

static void test_default_message_flags_call_order_and_32_bit_argument(void) {
    uint32_t state_a2ac_zero;
    uint32_t state_b2b0_zero;

    for (state_a2ac_zero = 0; state_a2ac_zero <= 1; state_a2ac_zero++) {
        for (state_b2b0_zero = 0; state_b2b0_zero <= 1; state_b2b0_zero++) {
            SchedulerEventReference state;
            const uint32_t message = 0x80100020u +
                (state_a2ac_zero << 1) + state_b2b0_zero;
            const uint32_t expected_flags =
                (state_a2ac_zero ? 2u : 0u) |
                (state_b2b0_zero ? 1u : 0u);

            scheduler_event_reference_init(&state, 0x80081000u);
            state.owner.count_2b4 = 7;
            state.owner.state_2ac = state_a2ac_zero ? 0 : 1;
            state.owner.state_2b0 = state_b2b0_zero ? 0 : 1;
            state.last_message = 0;
            state.check_result = expected_flags;
            scheduler_default_message_reference(&state, message);

            assert(state.owner.count_2b4 == 8);
            assert(state.prepare_seen_count == 8);
            assert(state.prepare_seen_message == message);
            assert(state.last_message == message);
            assert(state.call_count == 2);
            assert(state.calls[0].function == SCHEDULER_FUNC_07634);
            assert(state.calls[0].a0 == 0x80081000u);
            assert(state.calls[0].a1 == message);
            assert(state.calls[1].function == SCHEDULER_FUNC_077B8);
            assert(state.calls[1].a0 == 0x80081000u);
            assert(state.calls[1].a1 == 0x7FFFE024u);
            assert(state.calls[1].a2 == 0x7FFFE020u);
            assert(state.calls[1].a3 == expected_flags);
        }
    }
}

static void test_default_message_gate_and_conditional_start_call(void) {
    SchedulerEventReference gated;
    SchedulerEventReference start;
    const uint32_t message = 0x80345678u;

    scheduler_event_reference_init(&gated, 0x80082000u);
    gated.owner.state_2ac = 0;
    gated.owner.state_2b0 = 0;
    gated.last_message = 0;
    gated.check_result = 0;
    gated.global_gate_byte = 1;
    scheduler_default_message_reference(&gated, message);
    assert(gated.call_count == 2);
    assert(gated.calls[1].a3 == 3);

    scheduler_event_reference_init(&start, 0x80083000u);
    start.owner.state_2ac = 0;
    start.owner.state_2b0 = 0;
    start.last_message = 0;
    start.check_result = 0;
    start.global_gate_byte = 0;
    start.check_output_1 = 0x81000024u;
    start.check_output_2 = 0x82000020u;
    scheduler_default_message_reference(&start, message);
    assert(start.call_count == 3);
    assert(start.calls[0].function == SCHEDULER_FUNC_07634);
    assert(start.calls[1].function == SCHEDULER_FUNC_077B8);
    assert(start.calls[2].function == SCHEDULER_FUNC_0769C);
    assert(start.calls[2].a0 == 0x80083000u);
    assert(start.calls[2].a1 == 0x81000024u);
    assert(start.calls[2].a2 == 0x82000020u);
}

static void test_notification_sends_single_and_multiple_nodes(void) {
    SchedulerQueueReference empty;
    SchedulerQueueReference single;
    SchedulerQueueReference multiple;
    SchedulerQueueNode lone = {0, 0x81000000u};
    SchedulerQueueNode third = {0, 0x83000000u};
    SchedulerQueueNode second = {&third, 0x82000000u};
    SchedulerQueueNode first = {&second, 0x81000000u};
    const uint32_t notify[] = {SCHEDULER_MESSAGE_29D};

    scheduler_init(&empty, 0x8003F000u);
    scheduler_run_reference(&empty, notify, 1);
    assert(empty.trace_count == 1);
    assert(empty.trace[0].kind == SCHEDULER_TRACE_RECEIVE);

    scheduler_init(&single, 0x80040000u);
    single.list_head = &lone;
    scheduler_run_reference(&single, notify, 1);
    assert(single.trace_count == 2);
    assert(single.trace[1].kind == SCHEDULER_TRACE_SEND);
    assert(single.trace[1].arg0 == 0x81000000u);
    assert(single.trace[1].arg1 == 0x80040020u && single.trace[1].arg2 == 0);

    scheduler_init(&multiple, 0x80050000u);
    multiple.list_head = &first;
    scheduler_run_reference(&multiple, notify, 1);
    assert(multiple.trace_count == 4);
    assert(multiple.trace[1].kind == SCHEDULER_TRACE_SEND);
    assert(multiple.trace[1].arg0 == 0x81000000u);
    assert(multiple.trace[1].arg1 == 0x80050020u);
    assert(multiple.trace[2].kind == SCHEDULER_TRACE_SEND);
    assert(multiple.trace[2].arg0 == 0x82000000u);
    assert(multiple.trace[3].kind == SCHEDULER_TRACE_SEND);
    assert(multiple.trace[3].arg0 == 0x83000000u);
    assert(multiple.trace[1].arg2 == 0 && multiple.trace[2].arg2 == 0 &&
           multiple.trace[3].arg2 == 0);
}

static void test_callback_head_mutation_is_observed_by_next_event(void) {
    SchedulerQueueReference state;
    SchedulerQueueNode original = {0, 0x84000000u};
    SchedulerQueueNode replacement = {0, 0x85000000u};
    const uint32_t messages[] = {
        SCHEDULER_MESSAGE_29A,
        SCHEDULER_MESSAGE_29D,
    };

    scheduler_init(&state, 0x80060000u);
    state.list_head = &original;
    state.event_hook = replace_list_head_after_callback;
    state.event_hook_context = &replacement;
    scheduler_run_reference(&state, messages, 2);

    assert(state.trace_count == 4);
    assert(state.trace[1].kind == SCHEDULER_TRACE_CALLBACK);
    assert(state.trace[2].kind == SCHEDULER_TRACE_RECEIVE);
    assert(state.trace[3].kind == SCHEDULER_TRACE_SEND);
    assert(state.trace[3].arg0 == 0x85000000u);
    assert(state.trace[3].arg1 == 0x80060020u);
}

static void test_send_boundary_reloads_live_next_and_payload(void) {
    SchedulerQueueReference state;
    SchedulerQueueNode third = {0, 0x87000000u};
    SchedulerQueueNode second = {&third, 0x86000000u};
    SchedulerQueueNode first = {&second, 0x85000000u};
    SchedulerSendMutation mutation = {&third, 0x88000000u, 0};
    const uint32_t notify[] = {SCHEDULER_MESSAGE_29D};

    scheduler_init(&state, 0x80070000u);
    state.list_head = &first;
    state.send_hook = mutate_live_list_during_send;
    state.send_hook_context = &mutation;
    scheduler_run_reference(&state, notify, 1);

    assert(mutation.fired == 1);
    assert(state.trace_count == 3);
    assert(state.trace[1].kind == SCHEDULER_TRACE_SEND);
    assert(state.trace[1].arg0 == 0x85000000u);
    assert(state.trace[1].arg1 == 0x80070020u);
    assert(state.trace[2].kind == SCHEDULER_TRACE_SEND);
    assert(state.trace[2].arg0 == 0x88000000u);
    assert(state.trace[2].arg1 == 0x80070020u);
}

int main(void) {
    test_pointer_offsets_use_32_bit_guest_arithmetic();
    test_empty_queue_waits_without_dispatch();
    test_single_and_multiple_message_dispatch_order();
    test_notification_sends_single_and_multiple_nodes();
    test_callback_head_mutation_is_observed_by_next_event();
    test_send_boundary_reloads_live_next_and_payload();
    test_default_message_duplicate_still_increments_word_counter();
    test_default_message_flags_call_order_and_32_bit_argument();
    test_default_message_gate_and_conditional_start_call();
    return 0;
}
