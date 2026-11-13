#include <assert.h>
#include <stddef.h>
#include <stdint.h>
#include "object_flags.h"

typedef enum {
    OBJECT_FLAG_HELPER_7C90 = 1,
    OBJECT_FLAG_HELPER_A228,
    OBJECT_FLAG_HELPER_A5C4,
    OBJECT_FLAG_HELPER_A394,
} ObjectFlagHelper;

typedef struct {
    ObjectFlagHelper helper;
    ObjectFlagNode *arg0;
} ObjectFlagCall;

typedef struct {
    ObjectFlagCall calls[4];
    uint32_t call_count;
} ObjectFlagTrace;

static ObjectFlagTrace *active_production_trace;

static uint32_t record_helper(ObjectFlagTrace *trace, ObjectFlagHelper helper,
                              ObjectFlagNode *arg0) {
    uint32_t result;

    assert(trace->call_count < 4);
    trace->calls[trace->call_count].helper = helper;
    trace->calls[trace->call_count].arg0 = arg0;
    trace->call_count++;

    switch (helper) {
    case OBJECT_FLAG_HELPER_7C90:
        result = 0x7C900001u;
        break;
    case OBJECT_FLAG_HELPER_A228:
        result = 0xA2280002u;
        break;
    case OBJECT_FLAG_HELPER_A5C4:
        result = 0xA5C40003u;
        break;
    case OBJECT_FLAG_HELPER_A394:
        result = 0xA3940004u;
        break;
    default:
        assert(0);
        result = 0;
        break;
    }
    return result;
}

static void record_production_helper(ObjectFlagHelper helper, ObjectFlagNode *arg0) {
    assert(active_production_trace != 0);
    (void)record_helper(active_production_trace, helper, arg0);
}

void func_80007C90_8890(ObjectFlagNode *arg0) {
    record_production_helper(OBJECT_FLAG_HELPER_7C90, arg0);
}

void func_8000A228_AE28(ObjectFlagNode *arg0) {
    record_production_helper(OBJECT_FLAG_HELPER_A228, arg0);
}

void func_8000A5C4_B1C4(ObjectFlagNode *arg0) {
    record_production_helper(OBJECT_FLAG_HELPER_A5C4, arg0);
}

void func_8000A394_AF94(ObjectFlagNode *arg0) {
    record_production_helper(OBJECT_FLAG_HELPER_A394, arg0);
}

static void run_production_dispatch(ObjectFlagNode *node, ObjectFlagTrace *trace) {
    assert(active_production_trace == 0);
    active_production_trace = trace;
    func_80036308_36F08(node);
    active_production_trace = 0;
}

static void assert_same_trace(const ObjectFlagTrace *expected,
                             const ObjectFlagTrace *actual) {
    uint32_t i;

    assert(expected->call_count == actual->call_count);
    for (i = 0; i < expected->call_count; i++) {
        assert(expected->calls[i].helper == actual->calls[i].helper);
        assert(expected->calls[i].arg0 == actual->calls[i].arg0);
    }
}

/* Host reference for 80036308; helper bodies are opaque and side-effect free here. */
static uint32_t func_80036308_36F08_reference(ObjectFlagNode *arg0,
                                              uint32_t entry_v0,
                                              ObjectFlagTrace *trace) {
    uint8_t flags;
    uint8_t kind;

    if (arg0 == 0) {
        return entry_v0;
    }

    flags = arg0->flags;
    kind = (uint8_t)(flags & 0x7Fu);
    if (kind == 1) {
        record_helper(trace, OBJECT_FLAG_HELPER_7C90, arg0);
        return record_helper(trace, OBJECT_FLAG_HELPER_A228, arg0);
    }
    if (kind == 2) {
        return record_helper(trace, OBJECT_FLAG_HELPER_A5C4, arg0);
    }
    if (kind == 3) {
        return record_helper(trace, OBJECT_FLAG_HELPER_A394, arg0);
    }
    return flags;
}

static void test_list_flag_helper(void) {
    ObjectFlagNode c = {0, 0x81};
    ObjectFlagNode b = {&c, 0x20};
    ObjectFlagNode a = {&b, 0};
    ObjectFlagNode single = {0, 0x23};
    ObjectFlagOwner owner = {{0}, 0};

    _Static_assert(offsetof(ObjectFlagOwner, list) == 0x18, "owner list offset");
    assert(func_800362DC_36EDC(&owner) == 0);

    owner.list = &single;
    assert(func_800362DC_36EDC(&owner) == 0);
    assert(single.flags == 0xA3 && single.next == 0);

    owner.list = &a;
    assert(func_800362DC_36EDC(&owner) == 0);
    assert(a.flags == 0x80 && b.flags == 0xA0 && c.flags == 0x81);
    assert(a.next == &b && b.next == &c && c.next == 0);
}

static void test_single_node_dispatch(void) {
    ObjectFlagNode tail = {0, 0x5A};
    ObjectFlagNode node = {&tail, 0x81};
    ObjectFlagTrace trace = {{{0, 0}}, 0};
    ObjectFlagTrace actual = {{{0, 0}}, 0};
    uint8_t original_flags;

    original_flags = node.flags;
    assert(func_80036308_36F08_reference(&node, 0xDEADBEEFu, &trace) == 0xA2280002u);
    run_production_dispatch(&node, &actual);
    assert_same_trace(&trace, &actual);
    assert(trace.call_count == 2);
    assert(trace.calls[0].helper == OBJECT_FLAG_HELPER_7C90);
    assert(trace.calls[1].helper == OBJECT_FLAG_HELPER_A228);
    assert(trace.calls[0].arg0 == &node && trace.calls[1].arg0 == &node);
    assert(node.flags == original_flags && node.next == &tail);
    assert(tail.flags == 0x5A && tail.next == 0);
}

static void test_dispatch_kinds_and_unmatched_flags(void) {
    ObjectFlagNode node = {0, 0x82};
    ObjectFlagTrace trace = {{{0, 0}}, 0};
    ObjectFlagTrace actual = {{{0, 0}}, 0};
    uint8_t original_flags;

    original_flags = node.flags;
    assert(func_80036308_36F08_reference(&node, 0, &trace) == 0xA5C40003u);
    run_production_dispatch(&node, &actual);
    assert_same_trace(&trace, &actual);
    assert(trace.call_count == 1);
    assert(trace.calls[0].helper == OBJECT_FLAG_HELPER_A5C4);
    assert(trace.calls[0].arg0 == &node);
    assert(node.flags == original_flags && node.next == 0);

    node.flags = 0x83;
    original_flags = node.flags;
    trace.call_count = 0;
    actual.call_count = 0;
    assert(func_80036308_36F08_reference(&node, 0, &trace) == 0xA3940004u);
    run_production_dispatch(&node, &actual);
    assert_same_trace(&trace, &actual);
    assert(trace.call_count == 1);
    assert(trace.calls[0].helper == OBJECT_FLAG_HELPER_A394);
    assert(trace.calls[0].arg0 == &node);
    assert(node.flags == original_flags && node.next == 0);

    node.flags = 0x84;
    original_flags = node.flags;
    trace.call_count = 0;
    actual.call_count = 0;
    assert(func_80036308_36F08_reference(&node, 0, &trace) == original_flags);
    run_production_dispatch(&node, &actual);
    assert_same_trace(&trace, &actual);
    assert(trace.call_count == 0);
    assert(node.flags == original_flags && node.next == 0);

    node.flags = 0x05;
    original_flags = node.flags;
    trace.call_count = 0;
    actual.call_count = 0;
    assert(func_80036308_36F08_reference(&node, 0, &trace) == original_flags);
    run_production_dispatch(&node, &actual);
    assert_same_trace(&trace, &actual);
    assert(trace.call_count == 0);
    assert(node.flags == original_flags && node.next == 0);
}

static void test_null_preserves_entry_v0(void) {
    ObjectFlagTrace trace = {{{0, 0}}, 0};
    ObjectFlagTrace actual = {{{0, 0}}, 0};

    assert(func_80036308_36F08_reference(0, 0x13579BDFu, &trace) == 0x13579BDFu);
    run_production_dispatch(0, &actual);
    assert_same_trace(&trace, &actual);
    assert(trace.call_count == 0);
}

typedef struct ObjectListEntryReference {
    struct ObjectListEntryReference *next;
    uint32_t lookup_key;
} ObjectListEntryReference;

typedef struct {
    ObjectListEntryReference *head;
} ObjectListOwnerReference;

/* The original caller scans from head->next and checks null before calling 80036388. */
static ObjectListEntryReference *find_non_head_reference(ObjectListOwnerReference *owner,
                                                          uint32_t lookup_key) {
    ObjectListEntryReference *entry;

    if (owner == 0 || owner->head == 0) {
        return 0;
    }
    entry = owner->head->next;
    while (entry != 0) {
        if ((entry->lookup_key & 0x8FFFFFFEu) == (lookup_key & 0x8FFFFFFFu)) {
            return entry;
        }
        entry = entry->next;
    }
    return 0;
}

/* Only call for a non-head entry found in the list, matching the caller precondition. */
static uint32_t move_to_front_reference(ObjectListOwnerReference *owner,
                                        ObjectListEntryReference *target) {
    ObjectListEntryReference *previous;
    ObjectListEntryReference *entry;

    if (owner == 0 || target == 0) {
        return 0;
    }
    previous = owner->head;
    entry = previous->next;
    while (entry != target) {
        previous = entry;
        entry = entry->next;
    }
    if (entry != 0) {
        previous->next = target->next;
        target->next = owner->head;
        owner->head = target;
        return 1;
    }
    return 0;
}

static void test_move_caller_empty_singleton_and_no_match(void) {
    ObjectListEntryReference singleton = {0, 0x80000020u};
    ObjectListOwnerReference empty = {0};
    ObjectListOwnerReference one = {&singleton};

    assert(find_non_head_reference(&empty, 0x80000020u) == 0);
    assert(find_non_head_reference(&one, 0x80000020u) == 0);
    assert(find_non_head_reference(0, 0x80000020u) == 0);
    assert(move_to_front_reference(0, &singleton) == 0);
    assert(move_to_front_reference(&one, 0) == 0);
    assert(singleton.next == 0 && singleton.lookup_key == 0x80000020u);
}

static void test_move_to_front_preserves_other_fields(void) {
    ObjectListEntryReference tail = {0, 0x80000030u};
    ObjectListEntryReference middle = {&tail, 0x80000020u};
    ObjectListEntryReference head = {&middle, 0x80000010u};
    ObjectListOwnerReference owner = {&head};
    ObjectListEntryReference *found;

    assert(find_non_head_reference(&owner, 0x80000030u) == &tail);
    assert(move_to_front_reference(&owner, &tail) == 1);
    assert(owner.head == &tail);
    assert(tail.next == &head && head.next == &middle && middle.next == 0);
    assert(head.lookup_key == 0x80000010u);
    assert(middle.lookup_key == 0x80000020u);
    assert(tail.lookup_key == 0x80000030u);

    assert(find_non_head_reference(&owner, 0x80000010u) == &head);
    assert(find_non_head_reference(&owner, 0x80000020u) == &middle);
    assert(find_non_head_reference(&owner, 0x8FFFFFF0u) == 0);
    found = find_non_head_reference(&owner, 0x80000020u);
    assert(found == &middle);
    assert(move_to_front_reference(&owner, found) == 1);
    assert(owner.head == &middle && middle.next == &tail && tail.next == &head && head.next == 0);
    assert(head.lookup_key == 0x80000010u);
    assert(middle.lookup_key == 0x80000020u);
    assert(tail.lookup_key == 0x80000030u);
}

/* Reference case for 800363F4's non-head move-to-front relink contract. */
static void test_adjacent_owner_head_link_move_reference(void) {
    ObjectListEntryReference entry = {0, 0x80000020u};
    ObjectListEntryReference head = {&entry, 0x80000010u};
    ObjectListOwnerReference owner = {&head};
    ObjectListEntryReference *found;

    found = find_non_head_reference(&owner, 0x80000020u);
    assert(found == &entry);
    assert(move_to_front_reference(&owner, found) == 1);
    assert(owner.head == &entry && entry.next == &head && head.next == 0);
    assert(entry.lookup_key == 0x80000020u && head.lookup_key == 0x80000010u);
}

typedef struct ObjectAcquireReference {
    uint16_t current_count;
    uint16_t high_water;
    uint32_t side_effect_owner;
    uint16_t limit;
    int16_t used;
    uint32_t side_effect_result;
    ObjectFlagNode *allocation_result;
    uint32_t calls[2];
    uint32_t call_count;
    uint32_t side_effect_arg0;
    uint32_t side_effect_arg1;
    uint32_t allocation_arg;
    uint16_t count_at_side_effect;
    uint16_t count_at_allocator;
} ObjectAcquireReference;

enum {
    OBJECT_ACQUIRE_SIDE_EFFECT = 1,
    OBJECT_ACQUIRE_POOL_ALLOC = 2
};

/* Host reference for 80036448; helper and pool effects are observed by trace only. */
static ObjectFlagNode *func_80036448_reference(ObjectAcquireReference *state,
                                                ObjectFlagNode *unused_owner) {
    uint16_t next_count;

    (void)unused_owner;
    next_count = (uint16_t)(state->current_count + 1u);
    state->current_count = next_count;
    if (next_count > state->high_water) {
        state->high_water = next_count;
    }

    if (state->side_effect_owner != 0) {
        assert(state->call_count < 2);
        state->calls[state->call_count++] = OBJECT_ACQUIRE_SIDE_EFFECT;
        state->side_effect_arg0 = state->side_effect_owner;
        state->side_effect_arg1 = 1;
        state->count_at_side_effect = state->current_count;
        /* The original branches to allocation for either helper return value. */
        (void)state->side_effect_result;
    } else if ((int32_t)state->limit - (int32_t)state->used <= 0) {
        return 0;
    }

    assert(state->call_count < 2);
    state->calls[state->call_count++] = OBJECT_ACQUIRE_POOL_ALLOC;
    state->allocation_arg = 2;
    state->count_at_allocator = state->current_count;
    return state->allocation_result;
}

static void test_acquire_side_effect_then_pool_allocation(void) {
    ObjectFlagNode allocated = {0, 0};
    ObjectAcquireReference state = {7, 5, 0x12345678u, 0, 0, 0, &allocated,
                                    {0, 0}, 0, 0, 0, 0, 0, 0};
    ObjectFlagNode *result;

    result = func_80036448_reference(&state, &allocated);
    assert(result == &allocated);
    assert(state.current_count == 8 && state.high_water == 8);
    assert(state.call_count == 2);
    assert(state.calls[0] == OBJECT_ACQUIRE_SIDE_EFFECT);
    assert(state.calls[1] == OBJECT_ACQUIRE_POOL_ALLOC);
    assert(state.side_effect_arg0 == 0x12345678u && state.side_effect_arg1 == 1);
    assert(state.allocation_arg == 2);
    assert(state.count_at_side_effect == 8 && state.count_at_allocator == 8);
}

static void test_acquire_capacity_gate_and_signed_used_count(void) {
    ObjectFlagNode allocated = {0, 0};
    ObjectAcquireReference full = {4, 9, 0, 8, 8, 0, &allocated,
                                   {0, 0}, 0, 0, 0, 0, 0, 0};
    ObjectAcquireReference signed_boundary = {0xFFFFu, 0xFFFFu, 0, 0, -1, 0, 0,
                                              {0, 0}, 0, 0, 0, 0, 0, 0};

    assert(func_80036448_reference(&full, &allocated) == 0);
    assert(full.current_count == 5 && full.high_water == 9);
    assert(full.call_count == 0);

    /* The homed owner argument is not read; a null sentinel has the same result. */
    assert(func_80036448_reference(&signed_boundary, 0) == 0);
    assert(signed_boundary.current_count == 0);
    assert(signed_boundary.high_water == 0xFFFFu);
    assert(signed_boundary.call_count == 1);
    assert(signed_boundary.calls[0] == OBJECT_ACQUIRE_POOL_ALLOC);
    assert(signed_boundary.allocation_arg == 2);
    assert(signed_boundary.count_at_allocator == 0);
}

int main(void) {
    test_list_flag_helper();
    test_single_node_dispatch();
    test_dispatch_kinds_and_unmatched_flags();
    test_null_preserves_entry_v0();
    test_move_caller_empty_singleton_and_no_match();
    test_move_to_front_preserves_other_fields();
    test_adjacent_owner_head_link_move_reference();
    test_acquire_side_effect_then_pool_allocation();
    test_acquire_capacity_gate_and_signed_used_count();
    return 0;
}
