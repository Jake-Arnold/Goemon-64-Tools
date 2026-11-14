/* MIPS-derived host reference; the production target remains GLOBAL_ASM. */
#include <assert.h>
#include <stdint.h>

typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef int32_t s32;

enum {
    EVENT_TIMER = 1,
    EVENT_CURSOR_PREDICATE,
    EVENT_DELEGATE,
    EVENT_MESSAGE
};

static volatile u8 transition_memory[0xB000];
static volatile u8 save_state_memory[0xF8A4];
static volatile u16 global_gate;
static volatile u32 script_program_counter;

static int events[4];
static int event_count;
static int timer_calls;
static int cursor_calls;
static int delegate_calls;
static int message_calls;
static int mutate_rechecked_byte;

#define TRANSITION_U8(offset) (transition_memory[(offset)])
#define TRANSITION_U16(offset) \
    (*(volatile u16 *)(transition_memory + (offset)))

static void record_event(int event) {
    assert(event_count < (int)(sizeof(events) / sizeof(events[0])));
    events[event_count++] = event;
}

static void timer_helper(void) {
    timer_calls++;
    record_event(EVENT_TIMER);
}

static s32 cursor_nonzero_helper(void) {
    cursor_calls++;
    record_event(EVENT_CURSOR_PREDICATE);
    if (mutate_rechecked_byte) {
        /* Artificial ordering probe; no retail mutation across this call is known. */
        TRANSITION_U8(0xAE29) = 1;
    }
    return script_program_counter != 0;
}

static void delegate_helper(void) {
    delegate_calls++;
    record_event(EVENT_DELEGATE);
}

static void message_helper(s32 value) {
    assert(value == 3);
    assert(TRANSITION_U16(0xAE26) == 1);
    assert(TRANSITION_U8(0xADE0) == 0);
    assert(TRANSITION_U8(0xADE1) == 0);
    message_calls++;
    record_event(EVENT_MESSAGE);
}

/* Contract model copied from the verified branch order and widths. */
static void model_middle_transition_dispatch(void) {
    volatile u8 *transition;
    volatile u8 *save_state;
    u8 selector;

    timer_helper();
    transition = transition_memory + 0x7FFF;
    if (*(volatile u16 *)(transition + 0x2E27) != 0) {
        delegate_helper();
        return;
    }
    if ((global_gate & 0x1000) == 0) {
        return;
    }
    if (transition[0x2E2A] != 0) {
        return;
    }
    selector = transition[0x2DE5];
    if (selector == 3) {
        return;
    }
    if (selector >= 4) {
        return;
    }
    if (cursor_nonzero_helper() != 0) {
        return;
    }
    save_state = save_state_memory + 0x7FFF;
    if (save_state[0x78A3] != 0) {
        return;
    }
    if (transition[0x2E2A] != 0) {
        return;
    }
    if (save_state[0x788E] != 0) {
        return;
    }
    if (*(volatile u16 *)(transition + 0x2E17) != 0) {
        return;
    }
    *(volatile u16 *)(transition + 0x2E27) = 1;
    transition[0x2DE1] = 0;
    transition[0x2DE2] = 0;
    message_helper(3);
}

static void reset_fixture(void) {
    for (u32 i = 0; i < sizeof(transition_memory); i++) {
        transition_memory[i] = 0;
    }
    for (u32 i = 0; i < sizeof(save_state_memory); i++) {
        save_state_memory[i] = 0;
    }
    global_gate = 0;
    script_program_counter = 0;
    TRANSITION_U16(0xAE26) = 0;
    TRANSITION_U16(0xAE16) = 0;
    TRANSITION_U8(0xADE0) = 0x66;
    TRANSITION_U8(0xADE1) = 0x77;
    event_count = timer_calls = cursor_calls = delegate_calls = message_calls = 0;
    mutate_rechecked_byte = 0;
}

static void assert_timer_first(void) {
    assert(timer_calls == 1);
    assert(event_count >= 1 && events[0] == EVENT_TIMER);
}

static void assert_no_target_writes(u16 initial_halfword) {
    assert(TRANSITION_U16(0xAE26) == initial_halfword);
    assert(TRANSITION_U8(0xADE0) == 0x66);
    assert(TRANSITION_U8(0xADE1) == 0x77);
    assert(message_calls == 0);
}

static void test_busy_halfword_delegates_before_other_gates(void) {
    reset_fixture();
    TRANSITION_U16(0xAE26) = 0x1234;
    model_middle_transition_dispatch();
    assert_timer_first();
    assert(event_count == 2 && events[1] == EVENT_DELEGATE);
    assert(delegate_calls == 1 && cursor_calls == 0);
    assert_no_target_writes(0x1234);
}

static void test_early_gates_and_selector_boundaries(void) {
    reset_fixture();
    model_middle_transition_dispatch();
    assert_timer_first();
    assert(event_count == 1 && cursor_calls == 0);
    assert_no_target_writes(0);

    reset_fixture();
    global_gate = 0x1000;
    TRANSITION_U8(0xAE29) = 1;
    model_middle_transition_dispatch();
    assert_timer_first();
    assert(event_count == 1 && cursor_calls == 0);
    assert_no_target_writes(0);

    const u8 selectors[] = {3, 4, 255};
    for (u32 i = 0; i < sizeof(selectors) / sizeof(selectors[0]); i++) {
        reset_fixture();
        global_gate = 0x1000;
        TRANSITION_U8(0xADE4) = selectors[i];
        model_middle_transition_dispatch();
        assert_timer_first();
        assert(event_count == 1 && cursor_calls == 0);
        assert_no_target_writes(0);
    }
}

static void test_selector_zero_through_two_reach_cursor_gate(void) {
    for (u8 selector = 0; selector < 3; selector++) {
        reset_fixture();
        global_gate = 0x1000;
        TRANSITION_U8(0xADE4) = selector;
        script_program_counter = 0x80123400;
        model_middle_transition_dispatch();
        assert_timer_first();
        assert(event_count == 2 && events[1] == EVENT_CURSOR_PREDICATE);
        assert(cursor_calls == 1 && delegate_calls == 0);
        assert_no_target_writes(0);
    }
}

static void test_post_cursor_guards_preserve_fields(void) {
    reset_fixture();
    global_gate = 0x1000;
    save_state_memory[0xF8A2] = 1;
    model_middle_transition_dispatch();
    assert_timer_first();
    assert(event_count == 2 && events[1] == EVENT_CURSOR_PREDICATE);
    assert_no_target_writes(0);

    reset_fixture();
    global_gate = 0x1000;
    mutate_rechecked_byte = 1;
    model_middle_transition_dispatch();
    assert_timer_first();
    assert(event_count == 2 && events[1] == EVENT_CURSOR_PREDICATE);
    assert_no_target_writes(0);

    reset_fixture();
    global_gate = 0x1000;
    save_state_memory[0xF88D] = 1;
    model_middle_transition_dispatch();
    assert_timer_first();
    assert(event_count == 2 && events[1] == EVENT_CURSOR_PREDICATE);
    assert_no_target_writes(0);

    reset_fixture();
    global_gate = 0x1000;
    TRANSITION_U16(0xAE16) = 1;
    model_middle_transition_dispatch();
    assert_timer_first();
    assert(event_count == 2 && events[1] == EVENT_CURSOR_PREDICATE);
    assert_no_target_writes(0);
}

static void test_clear_path_writes_before_message_request(void) {
    reset_fixture();
    global_gate = 0x1000;
    model_middle_transition_dispatch();
    assert_timer_first();
    assert(event_count == 3);
    assert(events[1] == EVENT_CURSOR_PREDICATE);
    assert(events[2] == EVENT_MESSAGE);
    assert(cursor_calls == 1 && message_calls == 1 && delegate_calls == 0);
    assert(TRANSITION_U16(0xAE26) == 1);
    assert(TRANSITION_U8(0xADE0) == 0);
    assert(TRANSITION_U8(0xADE1) == 0);
}

int main(void) {
    test_busy_halfword_delegates_before_other_gates();
    test_early_gates_and_selector_boundaries();
    test_selector_zero_through_two_reach_cursor_gate();
    test_post_cursor_guards_preserve_fields();
    test_clear_path_writes_before_message_request();
    return 0;
}
