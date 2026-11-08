/* Synthetic VM-helper tests. Non-PIE keeps the indirect operand below 2 GiB. */
#define GOEMON_DECOMP_HOST_TEST
#include <assert.h>
#include <limits.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include "script_vm.c"

static u16 script0[] = {1, 2}, script1[] = {3, 4};
u16 *D_80077550_78150[] = {script0, NULL, script1};
u16 D_8007CCA4_7D8A4[] = {0xFFFF};
void *D_80077860_78460;
s32 D_801C7754_1C8354, D_801C7758_1C8358, D_801C775C_1C835C;
s32 D_801C7760_1C8360, D_801C7764_1C8364, D_801C7768_1C8368, D_801C776C_1C836C;
s32 D_801C77A0_1C83A0, D_801C77E0_1C83E0, D_801C77F4_1C83F4;
VmWork D_801C77E8_1C83E8;
s32 D_801C78EC_1C84EC, D_801C78F0_1C84F0;
s32 D_801C7900_1C8500, D_801C7904_1C8504;
s32 D_800779A0_785A0[0x6B];
s16 D_80078608_79208[0x6B];
u8 *D_801FC600_5B8510[3];
s8 D_801C78FC_1C84FC;
u8 D_801C7930_1C8530;

enum { RUN = 1, DRAW, RESET, INSTALL, CREATE, CLEANUP, DESTROY, SHOW, HIDE, POLL };
static s32 trace[32], trace_count, poll_result, args7[7], argument, state_at_poll;
static void *task_seen;
static VmTaskCallback callback;
static s32 memory_rhs;
VmControl D_8015CC30_15D830;
s32 D_801C78F4_1C84F4, D_801C78F8_1C84F8, D_801C77FC_1C83FC;
static int context_mode;
static s32 context_events[12], context_ids[12], context_event_count;
static void resource_event(s32 event, s32 value) {
    if (context_mode) {
        assert(context_event_count < 12);
        context_events[context_event_count] = event;
        context_ids[context_event_count++] = value;
    }
}
VmChoice D_801C7808_1C8408[10];
VmChoice *D_801C7800_1C8400;
VmInput D_801C7908_1C8508;
VmTaskCallback D_801C78D0_1C84D0;
static s32 flag_result, flag_calls;
static s32 emitted[16], emitted_count, emitted_owner;
static s16 *decoder_input, *decoder_output;
static s32 decoder_calls, decoder_owner;
static u16 feedback_ids[8];
static unsigned feedback_count;
static int override_buttons;
static u16 next_buttons;
void func_8000D060_DC60(s32 owner, s16 value) {
    assert(emitted_count < 16); emitted[emitted_count++] = value; emitted_owner = owner;
}
s16 *func_8003DF98_3EB98(s32 owner, s16 *script) {
    decoder_calls++; decoder_owner = owner; decoder_input = script;
    return decoder_output;
}
s32 func_800240DC_24CDC(s32 flag) {
    assert(flag == 0x82 && D_801C77E8_1C83E8.choice_state == 0);
    flag_calls++; return flag_result;
}
static VmWindow window0, window1;
VmWindow *D_80167C48_168848[] = {&window0, &window1};
VmPrompt D_801C78D8_1C84D8;
u8 D_80077150_77D50[4];
static SYS_W system_state;
SYS_W *D_8015C5C8_15D1C8 = &system_state;
s32 D_80077858_78458, D_8007785C_7845C;
s32 D_801C7770_1C8370, D_801C7774_1C8374;
u16 D_801C790C_1C850C;
u8 *D_801FC604_5B8514, *D_801FC608;
static s32 reset_args[2], cleanup_checks;
/* Independent scalar argument stubs; guest overlapping big-endian views are
 * validated by native byte matching, not modeled by this host ABI test. */
s32 D_801C7740_1C8340, D_801C7744_1C8344, D_801C78E8_1C84E8;
u16 D_801C7742_1C8342, D_801C78EA_1C84EA;
u8 D_801C7747_1C8347, D_801C774B_1C834B;
u32 D_801C7750_1C8350;
static u32 lookup_first, lookup_second, lookup_third;
static s32 lookup_count, lookup_ids[3], segment_id, segment_result, prepared;
static s32 forwarded[3], forward_kind;
s32 func_800141C4_14DC4(u32 resource) {
    assert(lookup_count < 3);
    resource_event(1, resource);
    lookup_ids[lookup_count++] = resource;
    return (s32)(lookup_count == 1 ? lookup_first : lookup_count == 2 ? lookup_second : lookup_third);
}
s32 func_80013B14_14714(s32 resource) {
    if (!context_mode) assert(lookup_count == 1 && !prepared);
    resource_event(2, resource); prepared = resource;
    D_801C78E8_1C84E8 = 2;
    return 0;
}
s32 func_80001E50_2A50(u32 resource) {
    if (!context_mode) assert(lookup_count == (lookup_first == 0xFFFFFFFF ? 2 : 1));
    resource_event(3, resource);
    segment_id = resource; return segment_result;
}
void func_80034EF8_35AF8(s32 a) { forward_kind = 1; forwarded[0] = a; }
void func_80038BC8_397C8(u16 a) { forward_kind = 2; forwarded[0] = a; }
void func_80038C30_39830(u16 a, u8 b, u8 c) {
    forward_kind = 3; forwarded[0] = a; forwarded[1] = b; forwarded[2] = c;
}
void func_80038B98_39798(u16 a) {
    forward_kind = 4; forwarded[0] = a;
    if (feedback_count < sizeof(feedback_ids) / sizeof(feedback_ids[0])) feedback_ids[feedback_count++] = a;
    if (override_buttons && a == 0x2B1) {
        D_801C7908_1C8508.button_pressed = D_801C790C_1C850C = next_buttons;
        override_buttons = 0;
    }
}
void func_80037C9C_3889C(s32 a, s32 b) { forward_kind = 5; forwarded[0] = a; forwarded[1] = b; }
void func_80037C20_38820(s32 a, s32 b, s32 c) {
    forward_kind = 6; forwarded[0] = a; forwarded[1] = b; forwarded[2] = c;
}
static void record(s32 event) { assert(trace_count < 32); trace[trace_count++] = event; }
static s32 dispatch_choice_calls, dispatch_prompt_calls, dispatch_tick_calls;
static s32 dispatch_last_x, dispatch_last_y;
void func_8003EBAC_3F7AC(s32 x, s32 y) {
    dispatch_choice_calls++;
    dispatch_last_x=x; dispatch_last_y=y;
}
void func_8003E234_3EE34(void) { dispatch_prompt_calls++; }
void func_8003ED60_3F960(void) { dispatch_tick_calls++; }

s32 func_8003D68C_3E28C(void) { record(RUN); return 0; }
void func_8003D0B0_3DCB0(void) { record(DRAW); }
void func_8003D468_3E068(s32 first, s32 second) {
    reset_args[0] = first; reset_args[1] = second;
    if (cleanup_checks) {
        assert(D_8007785C_7845C == 0x100 && D_801C77E8_1C83E8.marker == -1);
        assert(D_801C7930_1C8530 == 9);
    }
    record(RESET);
}
void func_8003521C_35E1C(VmTaskCallback value) { callback = value; task_seen = D_80077860_78460; record(INSTALL); }
s32 func_80034B24_35724(VmTaskCallback value, s32 arg) { callback = value; argument = arg; record(CREATE); return 0x1234; }
void func_8000C838_D438(void) {
    if (cleanup_checks) {
        assert(D_801C77E8_1C83E8.marker == -1 && D_8007785C_7845C == 7);
        assert(D_801C7930_1C8530 == 9);
    }
    record(CLEANUP);
}
void func_80035044_35C44(void *task) { assert(task == D_80077860_78460); task_seen = task; record(DESTROY); }
void func_8000C260_CE60(s32 a, s32 b, s32 c, s32 d, s32 e, s32 f, s32 g) {
    args7[0] = a; args7[1] = b; args7[2] = c; args7[3] = d;
    args7[4] = e; args7[5] = f; args7[6] = g; record(SHOW);
}
void func_8000C3A0_CFA0(s32 arg) { argument = arg; record(HIDE); }
s32 func_8000C314_CF14(s32 arg) { argument = arg; state_at_poll = D_801C77E0_1C83E0; record(POLL); return poll_result; }

_Static_assert(offsetof(VmWindow, field32) == 0x32, "window field32 offset");
_Static_assert(offsetof(VmWindow, field3e) == 0x3E, "window field3e offset");
_Static_assert(offsetof(VmWindow, field50) == 0x50, "window field50 offset");
_Static_assert(offsetof(VmWindow, field54) == 0x54, "window field54 offset");
_Static_assert(sizeof(VmPrompt) == 16, "prompt extent");
_Static_assert(offsetof(SYS_W, game_loops_count) == 0x3ADCE, "timer offset");
_Static_assert(offsetof(SYS_W, unk_cf8a0) == 0xCF8A0, "system tail offset preserved");
_Static_assert(offsetof(VmControl, flags) == 0xD4, "wait flag offset");
_Static_assert(offsetof(VmWaitOwner, resume) == 0xBC, "saved callback offset");
_Static_assert(sizeof(VmChoice) == 20, "choice record extent");
_Static_assert(offsetof(VmChoice, previous) == 8 && offsetof(VmChoice, next) == 12, "choice links");
_Static_assert(offsetof(VmChoice, script) == 16, "choice script offset");
_Static_assert(offsetof(VmInput, button_pressed) == 4 && offsetof(VmInput, stick_raw_x) == 6 && offsetof(VmInput, stick_raw_y) == 8, "input fields");
_Static_assert(offsetof(VmWork, last_direction) == 4 && offsetof(VmWork, repeat_ticks) == 6 && offsetof(VmWork, choice_state) == 12, "choice work fields");
_Static_assert(offsetof(VmWork, marker) == 8, "VM marker offset");
_Static_assert(offsetof(VmWork, countdown) == 0x10, "VM countdown offset");

static s32 relation(unsigned mode, s32 left, s32 right) {
    switch (mode) {
        case 0: return left == right;
        case 1: return left != right;
        case 2: return left < right;
        case 3: return left > right;
        case 4: return left <= right;
        default: return left >= right;
    }
}

static void check_comparisons(void) {
    const s32 values[] = {INT_MIN, -100, -1, 0, 1, 100, INT_MAX};
    const s32 modes[] = {0x8002, 0x8003, 0x800C, 0x800D, 0x800E, 0x800F};
    unsigned mode, a, b;
    uintptr_t pointer = (uintptr_t)&memory_rhs;
    assert(pointer <= INT_MAX && pointer % 4 == 0);
    for (mode = 0; mode < 6; mode++) {
        for (a = 0; a < sizeof(values) / sizeof(values[0]); a++) {
            for (b = 0; b < sizeof(values) / sizeof(values[0]); b++) {
                memory_rhs = values[b];
                assert(func_8003D9B8_3E5B8(modes[mode], values[a], values[b]) == relation(mode, values[a], values[b]));
                assert(func_8003D9B8_3E5B8((s32)(0x8030 + mode), values[a], (s32)pointer) == relation(mode, values[a], values[b]));
            }
        }
    }
    /* Unknown opcodes still need a valid indirect address in the original routine. */
    assert(func_8003D9B8_3E5B8(0, 1, (s32)pointer) == 0);
    assert(func_8003D9B8_3E5B8(0x8036, 1, (s32)pointer) == 0);
}

static void check_relocation_and_counters(void) {
    const s32 addresses[] = {INT_MIN, -1, 0, 1, 0x08000000, INT_MAX};
    const s32 deltas[] = {INT_MIN, -1, 0, 1, INT_MAX};
    unsigned a, b;
    for (a = 0; a < sizeof(addresses) / sizeof(addresses[0]); a++) {
        D_801C78EC_1C84EC = -1;
        D_801C78F0_1C84F0 = INT_MAX;
        assert(func_8003DE48_3EA48(addresses[a]) == addresses[a]);
        for (b = 0; b < sizeof(deltas) / sizeof(deltas[0]); b++) {
            s32 expected = addresses[a] < 0 ? addresses[a] : (s32)((u32)addresses[a] + (u32)deltas[b]);
            D_801C78EC_1C84EC = 0; D_801C78F0_1C84F0 = deltas[b];
            assert(func_8003DE48_3EA48(addresses[a]) == expected);
        }
    }
    for (a = 0; a < 4; a++) {
        D_801C77A0_1C83A0 = (s32)a;
        assert(func_8003DF68_3EB68() == (a >= 2));
        assert(D_801C77A0_1C83A0 == (s32)(a >= 2 ? a - 1 : a));
    }
    memset(&D_801C77E8_1C83E8, 0xA5, sizeof(VmWork));
    D_801C77E8_1C83E8.countdown = 2; D_801C77E0_1C83E0 = 7;
    func_8003E654_3F254(); assert(D_801C77E8_1C83E8.countdown == 1 && D_801C77E0_1C83E0 == 7);
    func_8003E654_3F254(); assert(D_801C77E8_1C83E8.countdown == 0 && D_801C77E0_1C83E0 == 0);
    D_801C77E0_1C83E0 = 7;
    func_8003E654_3F254(); assert(D_801C77E8_1C83E8.countdown == 0 && D_801C77E0_1C83E0 == 0);
    for (a = 0; a < 0x10; a++) assert(((u8 *)&D_801C77E8_1C83E8)[a] == 0xA5);
}

static void check_callbacks_and_dialogue_states(void) {
    static s32 task;
    unsigned i;
    assert(func_8003CFA0_3DBA0(0) == script0);
    assert(func_8003CFA0_3DBA0(1) == D_8007CCA4_7D8A4);
    assert(func_8003CFA0_3DBA0(2) == script1);
    trace_count = 0;
    func_8003D01C_3DC1C(&task, NULL);
    assert(D_80077860_78460 == &task && task_seen == &task && callback == func_8003CFD0_3DBD0);
    assert(trace_count == 2 && trace[0] == RESET && trace[1] == INSTALL && D_801C7930_1C8530 == 5);
    assert(reset_args[0] == 0 && reset_args[1] == -1);
    trace_count = 0;
    for (i = 0; i < 5; i++) func_8003CFD0_3DBD0(&task, NULL);
    assert(trace_count == 0 && D_801C7930_1C8530 == 0);
    func_8003CFD0_3DBD0(&task, NULL);
    assert(trace_count == 2 && trace[0] == RUN && trace[1] == DRAW);
    trace_count = 0; func_8003D058_3DC58();
    assert(trace_count == 1 && trace[0] == CREATE && argument == 0 && callback == func_8003D01C_3DC1C);
    trace_count = 0; func_8003D080_3DC80();
    assert(trace_count == 2 && trace[0] == CLEANUP && trace[1] == DESTROY && task_seen == &task && D_80077860_78460 == NULL);
    func_8003D44C_3E04C(); assert(D_801C78FC_1C84FC == 1);
    func_8003D45C_3E05C(); assert(D_801C78FC_1C84FC == 0);
    D_801C7754_1C8354 = 11; D_801C7758_1C8358 = 22; D_801C775C_1C835C = 33;
    D_801C7760_1C8360 = 44; D_801C7764_1C8364 = 55; D_801C7768_1C8368 = 66; D_801C776C_1C836C = 77;
    trace_count = 0; poll_result = 1; func_8003E548_3F148();
    for (i = 0; i < 7; i++) assert(args7[i] == (s32)((i + 1) * 11));
    assert(trace_count == 2 && trace[0] == SHOW && trace[1] == POLL && state_at_poll == 5 && D_801C77E0_1C83E0 == 5);
    poll_result = 0; func_8003E5EC_3F1EC(); assert(D_801C77E0_1C83E0 == 1);
    trace_count = 0; poll_result = 1; func_8003E5B8_3F1B8();
    assert(trace_count == 2 && trace[0] == HIDE && trace[1] == POLL && state_at_poll == 6 && D_801C77E0_1C83E0 == 6 && argument == 11);
    poll_result = 0; func_8003E620_3F220(); assert(D_801C77E0_1C83E0 == 1);
    func_8003EA0C_3F60C(); func_8003EBA4_3F7A4();
}

static void check_assignment_operands(void) {
    static u32 memory[4];
    static u32 words[4];
    const u32 literal_ops[] = {0x8009, 0x8016, 0x8017};
    unsigned i;
    s32 mode;
    /* Non-PIE static storage represents encoded 32-bit pointers. */
    for (mode = -1; mode <= 0; mode++) {
        D_801C78EC_1C84EC = mode;
        D_801C78F0_1C84F0 = mode == 0 ? 4 : 0;
        words[0] = (u32)(uintptr_t)&memory[1] - D_801C78F0_1C84F0;
        memory[0] = 0xAABBCCDD; memory[2] = 0x11223344; memory[3] = 0xDEADBEEF;
        for (i = 0; i < sizeof(literal_ops) / sizeof(literal_ops[0]); i++) {
            words[1] = literal_ops[i]; words[2] = 0x87654321;
            assert(func_8003DB0C_3E70C(words) == words + 3);
            assert(memory[1] == words[2]);
        }
        words[1] = 0x8013; words[2] = 1; memory[1] = 0xFFFFFFFF;
        assert(func_8003DB0C_3E70C(words) == words + 3 && memory[1] == 0);
        words[1] = 0x8014;
        assert(func_8003DB0C_3E70C(words) == words + 3 && memory[1] == 0xFFFFFFFF);
        words[1] = 0x8015;
        words[2] = (u32)(uintptr_t)&memory[2] - D_801C78F0_1C84F0;
        assert(func_8003DB0C_3E70C(words) == words + 3 && memory[1] == memory[2]);
        words[2] = words[0];
        assert(func_8003DB0C_3E70C(words) == words + 3 && memory[1] == memory[2]);
        for (i = 0x8008; i <= 0x8018; i++) {
            if (i == 0x8009 || (i >= 0x8013 && i <= 0x8017)) continue;
            words[1] = i;
            assert(func_8003DB0C_3E70C(words) == words + 2 && memory[1] == memory[2]);
        }
        assert(memory[0] == 0xAABBCCDD && memory[2] == 0x11223344 && memory[3] == 0xDEADBEEF);
    }
}

static void check_resource_address_resolution(void) {
    const u32 addresses[] = {0, 0x02000024, 0xFFFFFFFF};
    const u32 bases[] = {0, 0x40001234, 0x80005000, 0xFFFFFFFF};
    const s32 segments[] = {0, 2, 0x80, -1};
    unsigned a, b, c;
    for (a = 0; a < sizeof(addresses) / sizeof(addresses[0]); a++) {
        for (b = 0; b < sizeof(bases) / sizeof(bases[0]); b++) {
            for (c = 0; c < sizeof(segments) / sizeof(segments[0]); c++) {
                u32 expected_base = bases[b] == 0xFFFFFFFF ? 0xC0001000 : bases[b];
                lookup_count = 0; lookup_first = bases[b]; lookup_second = 0xC0001000;
                segment_result = segments[c]; prepared = 0; segment_id = 0;
                D_801C78E8_1C84E8 = 0; D_801C78EA_1C84EA = 0xFEDC;
                assert(func_8003DDC4_3E9C4(addresses[a], 7) ==
                    addresses[a] - ((u32)segments[c] << 24) + (expected_base & 0xBFFFFFFF));
                assert(lookup_ids[0] == 7 && segment_id == 7);
                if (bases[b] == 0xFFFFFFFF) {
                    assert(lookup_count == 2 && prepared == 0xFEDC && lookup_ids[1] == 2);
                } else assert(lookup_count == 1 && prepared == 0);
            }
        }
    }
    /* A failed fallback lookup also follows the original arithmetic. */
    lookup_count = 0; lookup_first = lookup_second = 0xFFFFFFFF;
    segment_result = 0; prepared = 0;
    assert(func_8003DDC4_3E9C4(0, 7) == 0xBFFFFFFF);
}

static void check_operand_callbacks(void) {
    const s32 operands[] = {INT_MIN, -1, 0, 1, 0x7FFF, 0x8000, 0xFFFF, INT_MAX};
    unsigned a, b;
    for (a = 0; a < sizeof(operands) / sizeof(operands[0]); a++) {
        D_801C7740_1C8340 = operands[a];
        for (b = 0; b < sizeof(operands) / sizeof(operands[0]); b++) {
            D_801C7744_1C8344 = operands[b];
            func_8003F524_40124();
            assert(D_801C7750_1C8350 == (u32)operands[a] + (u32)operands[b]);
            func_8003F544_40144();
            assert(D_801C7750_1C8350 == (u32)operands[a] - (u32)operands[b]);
        }
        memset(&D_801C77E8_1C83E8, 0xA5, sizeof(VmWork));
        func_8003F460_40060();
        assert(D_801C77E8_1C83E8.countdown == operands[a] && D_801C77E0_1C83E0 == 7);
        func_8003F5FC_401FC(42);
        assert(D_801C77E8_1C83E8.countdown == 42 && D_801C77E0_1C83E0 == 7);
        for (b = 0; b < 0x10; b++) assert(((u8 *)&D_801C77E8_1C83E8)[b] == 0xA5);
        func_8003F43C_4003C(); assert(forward_kind == 1 && forwarded[0] == operands[a]);
        func_8003F660_40260();
        assert(forward_kind == 4 && forwarded[0] == (u16)((u32)operands[a] + 0x8000));
        func_8003F694_40294(); assert(forward_kind == 5 && forwarded[0] == 0 && forwarded[1] == operands[a]);
        func_8003F6BC_402BC();
        assert(forward_kind == 6 && forwarded[0] == 0 && forwarded[1] == 1 && forwarded[2] == operands[a]);
    }
    D_801C7742_1C8342 = 0xFEDC; D_801C7747_1C8347 = 0xFE; D_801C774B_1C834B = 0xDC;
    func_8003F608_40208(); assert(forward_kind == 2 && forwarded[0] == 0xFEDC);
    func_8003F62C_4022C();
    assert(forward_kind == 3 && forwarded[0] == 0xFEDC && forwarded[1] == 0xFE && forwarded[2] == 0xDC);
}

static void check_input_gate_and_cleanup(void) {
    const u16 inputs[] = {0, 0x4000, 0x8000, 0xC000, 1, 0x4001, 0x8001, 0xC001};
    const s32 targets[] = {0, 0x100, -1, INT_MIN, INT_MAX};
    unsigned i, j, busy, active, handler;
    static u8 owner[0x60];
    for (handler = 0; handler < 2; handler++) for (i = 0; i < sizeof(inputs) / sizeof(inputs[0]); i++) {
        for (j = 0; j < sizeof(targets) / sizeof(targets[0]); j++) {
            for (busy = 0; busy < 2; busy++) for (active = 0; active < 2; active++) {
                trace_count = 0; cleanup_checks = 0;
                D_801C790C_1C850C = inputs[i]; D_801C7770_1C8370 = busy;
                D_801C7774_1C8374 = targets[j]; D_801C77E0_1C83E0 = 99;
                D_801C78EC_1C84EC = active ? 0 : -1; D_801C78F0_1C84F0 = 0x40;
                D_80077858_78458 = 1234; D_8007785C_7845C = 7;
                memset(&D_801C77E8_1C83E8, 0xA5, sizeof(VmWork));
                D_801C77E8_1C83E8.countdown = 123456;
                D_801C77E8_1C83E8.marker = 55; D_801C7930_1C8530 = 9;
                if (!(inputs[i] & 0x8000) && (inputs[i] & 0x4000) && !busy && !targets[j]) cleanup_checks = 1;
                D_80077860_78460 = owner; owner[0x5D] = 42;
                system_state.game_loops_count = 1;
                D_801C78D8_1C84D8.pattern = 1;
                if (handler) func_8003E3EC_3EFEC(); else func_8003E4C0_3F0C0();
                assert(D_801C78D8_1C84D8.pattern == (handler ? 0x80000000 : 1));
                assert(owner[0x5D] == 42);
                if (inputs[i] & 0x8000) {
                    assert(D_801C77E0_1C83E0 == 1 && trace_count == 0 && D_80077858_78458 == 1234);
                } else if ((inputs[i] & 0x4000) && !busy) {
                    assert(D_801C77E0_1C83E0 == 0);
                    if (targets[j] == 0) {
                        assert(trace_count == 2 && trace[0] == CLEANUP && trace[1] == RESET);
                        assert(reset_args[0] == 0 && reset_args[1] == -1);
                        assert(D_801C7930_1C8530 == 3 && D_801C77E8_1C83E8.marker == -1 && D_8007785C_7845C == 0x100);
                    } else {
                        s32 expected = targets[j] < 0 ? targets[j] : (s32)((u32)targets[j] + (active ? 0x40U : 0U));
                        assert(D_80077858_78458 == expected && trace_count == 0);
                    }
                } else assert(D_801C77E0_1C83E0 == 99 && trace_count == 0 && D_80077858_78458 == 1234);
                assert(D_801C77E8_1C83E8.countdown == 123456);
                {
                    unsigned byte;
                    for (byte = 0; byte < 0x10; byte++) if (byte != 8 && byte != 9)
                        assert(((u8 *)&D_801C77E8_1C83E8)[byte] == 0xA5);
                }
                if (!cleanup_checks) assert(D_801C7930_1C8530 == 9 && D_801C77E8_1C83E8.marker == 55 && D_8007785C_7845C == 7);
            }
        }
    }
    cleanup_checks = 0;
}

static void check_control_queries(void) {
    static s32 next_word = (s32)0x87654321;
    u8 actor[0x62];
    const s32 owners[] = {INT_MIN, -1, 0, 1, 2, 0x12345, INT_MAX};
    const s16 markers[] = {-32768, -1, 0, 1, 32767};
    unsigned i, j;
    D_80077858_78458 = 0; assert(func_8003F1D8_3FDD8() == 0);
    D_80077858_78458 = -1; assert(func_8003F1D8_3FDD8() == 1);
    for (i = 0; i < sizeof(owners) / sizeof(owners[0]); i++) for (j = 0; j < sizeof(markers) / sizeof(markers[0]); j++) {
        s32 owner = owners[i] & ~1;
        D_801C7768_1C8368 = owners[i]; D_801C77E8_1C83E8.marker = markers[j];
        assert(func_8003F1FC_3FDFC(owner) == markers[j]);
        assert(func_8003F1FC_3FDFC(owner ^ 1) == -1);
    }
    D_80077858_78458 = (s32)(intptr_t)&next_word; D_801C78E8_1C84E8 = 0x12345678; trace_count = 0;
    assert(func_8003F1D8_3FDD8() == 1);
    func_8003F564_40164();
    assert(trace_count == 1 && trace[0] == RESET && reset_args[0] == next_word && reset_args[1] == 0x12345678);
    D_801FC604_5B8514 = D_801FC608 = NULL;
    func_8003F594_40194(); assert(D_801C7750_1C8350 == 0xFFFFFFFF);
    func_8003F5C8_401C8(); assert(D_801C7750_1C8350 == 0xFFFFFFFF);
    memset(actor, 0xA5, sizeof(actor));
    for (i = 0; i < 256; i++) {
        actor[0x60] = (u8)i;
        D_801FC604_5B8514 = actor; D_801FC608 = NULL;
        func_8003F594_40194(); assert(D_801C7750_1C8350 == i);
        func_8003F5C8_401C8(); assert(D_801C7750_1C8350 == 0xFFFFFFFF);
        D_801FC604_5B8514 = NULL; D_801FC608 = actor;
        func_8003F5C8_401C8(); assert(D_801C7750_1C8350 == i);
        func_8003F594_40194(); assert(D_801C7750_1C8350 == 0xFFFFFFFF);
        for (j = 0; j < sizeof(actor); j++) if (j != 0x60) assert(actor[j] == 0xA5);
    }
    D_801FC604_5B8514 = D_801FC608 = NULL;
}

static void check_prompt_geometry_and_animation(void) {
    VmWindow before;
    static u8 owner[0x60];
    unsigned i, low;
    memset(&window0, 0xA5, sizeof(window0));
    window0.field32 = 50; window0.field3e = 7; window0.field50 = 3;
    window0.field34 = 60; window0.field40 = 3; window0.field42 = 5; window0.field54 = 8;
    before = window0; D_801C7754_1C8354 = 0; trace_count = 0;
    func_8003E1A8_3EDA8();
    assert(D_801C78D8_1C84D8.x == 40 && D_801C78D8_1C84D8.y == 55);
    assert(D_801C78D8_1C84D8.texture == (u32)(uintptr_t)D_80077150_77D50);
    assert(D_801C78D8_1C84D8.pattern == 0xFF00FF && D_801C77E0_1C83E0 == 3);
    assert(memcmp(&before, &window0, sizeof(window0)) == 0 && trace_count == 0);
    memset(&window1, 0x5A, sizeof(window1));
    window1.field32 = -32768; window1.field3e = -32768; window1.field50 = INT_MAX;
    window1.field34 = -32768; window1.field40 = -32768; window1.field42 = -32768; window1.field54 = INT_MIN;
    before = window1; D_801C7754_1C8354 = 1;
    func_8003E1A8_3EDA8();
    assert((u32)D_801C78D8_1C84D8.x == 0x7FFEFFF3);
    assert((u32)D_801C78D8_1C84D8.y == 0xBFFF7FF4);
    assert(memcmp(&before, &window1, sizeof(window1)) == 0);
    D_801C790C_1C850C = 0; D_801C7770_1C8370 = 1;
    D_80077860_78460 = owner; system_state.game_loops_count = 1;
    for (i = 0; i < 32; i++) {
        D_801C78D8_1C84D8.pattern = 1U << i;
        func_8003E3EC_3EFEC();
        assert(D_801C78D8_1C84D8.pattern == (1U << ((i + 31) % 32)));
    }
    D_801C78D8_1C84D8.pattern = 0xA5C30001;
    func_8003E3EC_3EFEC(); assert(D_801C78D8_1C84D8.pattern == 0xD2E18000);
    for (i = 1; i < 32; i++) func_8003E3EC_3EFEC();
    assert(D_801C78D8_1C84D8.pattern == 0xA5C30001);
    for (low = 0; low < 16; low++) for (i = 0; i < 256; i++) {
        unsigned byte;
        memset(owner, 0xA5, sizeof(owner)); owner[0x5D] = (u8)i;
        system_state.game_loops_count = 0xFFF0 | low;
        func_8003E3EC_3EFEC();
        assert(owner[0x5D] == (u8)(i + (low == 0)));
        for (byte = 0; byte < sizeof(owner); byte++) if (byte != 0x5D) assert(owner[byte] == 0xA5);
    }
    assert((u32)D_801C78D8_1C84D8.x == 0x7FFEFFF3 && (u32)D_801C78D8_1C84D8.y == 0xBFFF7FF4);
    assert(D_801C78D8_1C84D8.texture == (u32)(uintptr_t)D_80077150_77D50);
}

static void check_choice_directions_and_repeat(void) {
    static const struct { s16 x, y; u16 pressed, expected; } cases[] = {
        {0, 0, 0, 0}, {-40, 40, 0, 0}, {40, -40, 0, 0},
        {-41, 0, 0, 0x800}, {0, 41, 0, 0x800}, {41, 0, 0, 0x400}, {0, -41, 0, 0x400},
        {-32768, 32767, 0, 0x800}, {32767, -32768, 0, 0x400},
        {41, 41, 0, 0x800}, {-41, -41, 0, 0x800}, {0, 0, 0xF00, 0x800},
        {0, 0, 0xA00, 0x800}, {0, 0, 0x500, 0x400}, {0, 0, 0xC001, 0}
    };
    unsigned i, tick;
    for (i = 0; i < sizeof(cases) / sizeof(cases[0]); i++) {
        memset(&D_801C77E8_1C83E8, 0xA5, sizeof(VmWork));
        D_801C77E8_1C83E8.last_direction = 0x1234; D_801C77E8_1C83E8.repeat_ticks = 99;
        D_801C7908_1C8508.stick_raw_x = cases[i].x; D_801C7908_1C8508.stick_raw_y = cases[i].y;
        D_801C7908_1C8508.button_pressed = cases[i].pressed;
        assert(func_8003EA14_3F614() == cases[i].expected);
        assert(D_801C77E8_1C83E8.last_direction == cases[i].expected && D_801C77E8_1C83E8.repeat_ticks == 0);
        for (tick = 0; tick < 10; tick++) {
            assert(func_8003EA14_3F614() == 0);
            assert(D_801C77E8_1C83E8.repeat_ticks == tick + 1);
        }
        assert(func_8003EA14_3F614() == cases[i].expected && D_801C77E8_1C83E8.repeat_ticks == 0);
        D_801C77E8_1C83E8.repeat_ticks = 0xFFFF;
        assert(func_8003EA14_3F614() == cases[i].expected && D_801C77E8_1C83E8.repeat_ticks == 0);
        for (tick = 0; tick < sizeof(VmWork); tick++) if (tick < 4 || tick >= 8)
            assert(((u8 *)&D_801C77E8_1C83E8)[tick] == 0xA5);
    }
    D_801C7908_1C8508.stick_raw_x = D_801C7908_1C8508.stick_raw_y = 0;
    D_801C7908_1C8508.button_pressed = 0x800;
    D_801C77E8_1C83E8.last_direction = 0;
    assert(func_8003EA14_3F614() == 0x800);
    D_801C7908_1C8508.button_pressed = 0x400;
    assert(func_8003EA14_3F614() == 0x400 && D_801C77E8_1C83E8.repeat_ticks == 0);
}

static void set_choice_buttons(u16 buttons) {
    /* These views alias on the guest; keep synthetic integration inputs consistent. */
    D_801C7908_1C8508.button_pressed = D_801C790C_1C850C = buttons;
}

static void reset_choice_fixture(void) {
    static u8 owner[0x60];
    unsigned i;
    memset(D_801C7808_1C8408, 0, sizeof(D_801C7808_1C8408));
    for (i = 0; i < 3; i++) {
        VmChoice *node = &D_801C7808_1C8408[i];
        node->previous = i ? VM_U32_ADDRESS(node - 1) : 0;
        node->next = i < 2 ? VM_U32_ADDRESS(node + 1) : 0;
        node->script = 0x80001000U + i * 0x100;
    }
    memset(owner, 0xA5, sizeof(owner)); D_80077860_78460 = owner;
    system_state.game_loops_count = 1;
    memset(&D_801C7908_1C8508, 0, sizeof(VmInput));
    D_801C790C_1C850C = 0; D_801C7770_1C8370 = 0;
    D_801C77E8_1C83E8.choice_state = 1; D_801C77E8_1C83E8.last_direction = 0;
    D_801C77E8_1C83E8.repeat_ticks = 0; D_801C77E0_1C83E0 = 2;
    D_801C7800_1C8400 = &D_801C7808_1C8408[1];
    D_80077858_78458 = 0x1234; D_801C78D0_1C84D0 = func_8003CFD0_3DBD0;
    feedback_count = 0; flag_calls = 0; flag_result = 0; override_buttons = 0;
}

static void check_choice_navigation_and_confirmation(void) {
    unsigned i, busy, enabled;
    for (i = 0; i < 3; i++) {
        reset_choice_fixture(); D_801C7800_1C8400 = &D_801C7808_1C8408[i];
        set_choice_buttons(0x800);
        assert(func_8003EACC_3F6CC(D_801C7800_1C8400) == (i ? -1 : 0));
        D_801C77E8_1C83E8.last_direction = 0;
        set_choice_buttons(0x400);
        assert(func_8003E888_3F488(D_801C7808_1C8408) == 0);
        assert(D_801C7800_1C8400 == &D_801C7808_1C8408[i < 2 ? i + 1 : i]);
        assert(feedback_count == (unsigned)(i < 2));
        if (feedback_count) assert(feedback_ids[0] == 0x2B1);
    }
    reset_choice_fixture(); set_choice_buttons(0x800);
    assert(func_8003E888_3F488(D_801C7808_1C8408) == 0 && D_801C7800_1C8400 == &D_801C7808_1C8408[0]);
    for (busy = 0; busy < 2; busy++) for (enabled = 0; enabled < 2; enabled++) {
        reset_choice_fixture(); D_801C7770_1C8370 = busy; flag_result = enabled ? 4 : 0;
        set_choice_buttons(0xC400);
        func_8003E81C_3F41C();
        assert(D_801C7800_1C8400 == &D_801C7808_1C8408[2]);
        assert((u32)D_80077858_78458 == 0x80001200 && D_801C77E0_1C83E0 == 0);
        assert(D_801C78D0_1C84D0 == NULL && D_801C77E8_1C83E8.choice_state == 0);
        assert(flag_calls == 1 && feedback_ids[0] == 0x2B1);
        assert(feedback_count == (enabled ? 1U : 2U));
        if (!enabled) assert(feedback_ids[1] == 0x2B0);
    }
    for (busy = 0; busy < 2; busy++) {
        reset_choice_fixture(); D_801C7770_1C8370 = busy; set_choice_buttons(0x4000);
        func_8003E81C_3F41C();
        assert(D_80077858_78458 == (busy ? 0x1234 : 0x1238));
        assert(D_801C77E0_1C83E0 == (busy ? 2 : 0) && flag_calls == 0 && feedback_count == 0);
        assert((D_801C78D0_1C84D0 == NULL) == !busy);
    }
    reset_choice_fixture(); set_choice_buttons(0x400);
    override_buttons = 1; next_buttons = 0x8000;
    func_8003E81C_3F41C();
    assert(D_801C7800_1C8400 == &D_801C7808_1C8408[2]);
    assert((u32)D_80077858_78458 == 0x80001200 && flag_calls == 1 && feedback_count == 2);
    reset_choice_fixture(); D_80077858_78458 = -1; set_choice_buttons(0x4000);
    assert(func_8003E888_3F488(D_801C7808_1C8408) == -1 && D_80077858_78458 == 3);
    reset_choice_fixture(); D_801C77E8_1C83E8.choice_state = 0; set_choice_buttons(0x8000);
    func_8003E81C_3F41C();
    assert(D_801C7800_1C8400 == D_801C7808_1C8408 && D_801C77E8_1C83E8.choice_state == 1);
    assert(D_801C77E8_1C83E8.last_direction == 0 && D_801C77E8_1C83E8.repeat_ticks == 0);
    assert(D_80077858_78458 == 0x1234 && D_801C77E0_1C83E0 == 2 && flag_calls == 0);
    reset_choice_fixture(); set_choice_buttons(0xF00);
    D_801C7800_1C8400 = D_801C7808_1C8408;
    assert(func_8003EACC_3F6CC(D_801C7800_1C8400) == 0);
    for (i = 0; i < 512; i++) {
        unsigned byte;
        u8 *owner;
        reset_choice_fixture(); D_801C77E8_1C83E8.choice_state = 2;
        system_state.game_loops_count = i & 1;
        owner = D_80077860_78460; owner[0x5C] = (u8)(i / 2);
        assert(func_8003E888_3F488(D_801C7808_1C8408) == 0);
        assert(owner[0x5C] == (u8)(i / 2 + ((i & 1) ? 0 : 2)));
        for (byte = 0; byte < 0x60; byte++) if (byte != 0x5C) assert(owner[byte] == 0xA5);
        assert(D_801C77E8_1C83E8.choice_state == 2 && flag_calls == 0 && feedback_count == 0);
    }
    memset(&D_801C77E8_1C83E8, 0xA5, sizeof(VmWork));
    func_8003E9E8_3F5E8(NULL);
    assert(D_801C7800_1C8400 == NULL && D_801C77E8_1C83E8.choice_state == 1);
    assert(D_801C77E8_1C83E8.last_direction == 0 && D_801C77E8_1C83E8.repeat_ticks == 0);
    for (i = 0; i < sizeof(VmWork); i++) if (i < 4 || (i >= 8 && i < 12) || i >= 16)
        assert(((u8 *)&D_801C77E8_1C83E8)[i] == 0xA5);
}

static void check_choice_stream_rendering(void) {
    s16 first[] = {0, 0x7FFF, -2, -1};
    s16 second[] = {42, -1};
    s16 empty[] = {-1};
    emitted_count = decoder_calls = 0; decoder_output = second;
    func_8003EB34_3F734(17, first);
    assert(emitted_count == 3 && emitted[0] == 0 && emitted[1] == 0x7FFF && emitted[2] == 42 && emitted_owner == 17);
    assert(decoder_calls == 1 && decoder_owner == 17 && decoder_input == first + 2);
    emitted_count = decoder_calls = 0;
    func_8003EB34_3F734(18, empty); assert(emitted_count == 0 && decoder_calls == 0);
    first[0] = (s16)0x8000; decoder_output = empty;
    func_8003EB34_3F734(19, first); assert(emitted_count == 0 && decoder_calls == 1 && decoder_input == first);
}

static void check_choice_index_and_wait_callbacks(void) {
    const u32 flags[] = {0, 1, 0xFFFFFFFE, 0xFFFFFFFF, 0x80000000};
    const s32 pending[] = {0, 1, -1, INT_MIN, INT_MAX};
    static VmWaitOwner owner;
    unsigned i, j;
    D_801C77E0_1C83E0 = 2;
    for (i = 0; i < 10; i++) {
        D_801C7800_1C8400 = &D_801C7808_1C8408[i];
        assert(func_8003F0FC_3FCFC() == (s32)i);
    }
    D_801C7800_1C8400 = NULL; assert(func_8003F0FC_3FCFC() == 10);
    for (i = 0; i < 5; i++) {
        D_801C77E0_1C83E0 = pending[i];
        assert(func_8003F0FC_3FCFC() == -1);
    }
    memset(&owner, 0xA5, sizeof(owner));
    owner.resume = VM_U32_ADDRESS(func_8003CFD0_3DBD0);
    D_80077860_78460 = &owner;
    for (i = 0; i < sizeof(flags) / sizeof(flags[0]); i++) {
        memset(&D_8015CC30_15D830, 0x5A, sizeof(VmControl));
        D_8015CC30_15D830.flags = flags[i]; trace_count = 0;
        func_8003F14C_3FD4C(&owner, NULL);
        assert(D_8015CC30_15D830.flags == (flags[i] | 1U));
        assert(trace_count == 1 && trace[0] == INSTALL && callback == func_8003F18C_3FD8C);
        for (j = 0; j < 0xD4; j++) assert(D_8015CC30_15D830.unknown00[j] == 0x5A);
        for (j = 0; j < sizeof(pending) / sizeof(pending[0]); j++) {
            D_80077858_78458 = pending[j]; D_8015CC30_15D830.flags = flags[i];
            callback = func_8003F18C_3FD8C; trace_count = 0;
            func_8003F18C_3FD8C(&owner, NULL);
            if (!pending[j]) {
                assert(D_8015CC30_15D830.flags == (flags[i] & ~1U));
                assert(trace_count == 1 && trace[0] == INSTALL && callback == func_8003CFD0_3DBD0);
            } else assert(D_8015CC30_15D830.flags == flags[i] && trace_count == 0 && callback == func_8003F18C_3FD8C);
        }
        for (j = 0; j < 0xBC; j++) assert(owner.unknown00[j] == 0xA5);
    }
}

static void setup_context_fixture(u32 first, u32 second, s32 segment) {
    context_mode = 1; context_event_count = 0; lookup_count = 0; prepared = 0;
    lookup_first = first; lookup_second = second; lookup_third = 0x80003000;
    segment_result = segment;
}

static void check_resource_context_transitions(void) {
    const s32 addresses[] = {0x02000024, -1, INT_MIN, INT_MAX};
    unsigned i;
    for (i = 0; i < sizeof(addresses) / sizeof(addresses[0]); i++) {
        u32 resolved = (u32)addresses[i] - 0x02000000U + 0x80001000U;
        s32 expected = addresses[i] < 0 ? addresses[i] : (s32)resolved;
        D_80077858_78458 = (s32)0x80005000; D_801C78E8_1C84E8 = 7;
        D_801C7744_1C8344 = 9; D_801C7740_1C8340 = addresses[i];
        setup_context_fixture(0xC0001000, 0xC0001000, 2);
        func_8003F23C_3FE3C();
        assert(D_801C78F4_1C84F4 == (s32)0x80005000 && D_801C78F8_1C84F8 == 7);
        assert(D_801C78E8_1C84E8 == 9 && (u32)D_801C77FC_1C83FC == 0xC0001000);
        assert(D_801C78EC_1C84EC == 2 && (u32)D_801C78F0_1C84F0 == 0x7E001000);
        assert(D_80077858_78458 == expected);
        assert(context_event_count == 4 && context_events[0] == 1 && context_events[1] == 3 && context_events[2] == 1 && context_events[3] == 3);
        assert(context_ids[0] == 9 && context_ids[1] == 9 && context_ids[2] == 9 && context_ids[3] == 9);
        setup_context_fixture(0x80007000, 0x80007000, -1);
        func_8003F2D4_3FED4();
        assert(D_801C78E8_1C84E8 == 7 && D_801C78EC_1C84EC == -1);
        assert((u32)D_801C77FC_1C83FC == 0x80007000 && D_80077858_78458 == (s32)0x80005000);
        assert(context_event_count == 4 && context_ids[0] == 7 && context_ids[1] == 7 && context_ids[2] == 7 && context_ids[3] == 7);
        assert(D_801C78F8_1C84F8 == 7 && D_801C78F4_1C84F4 == (s32)0x80005000);
    }
    /* Resolver fallback reloads the current resource changed by preparation. */
    D_80077858_78458 = 1234; D_801C78E8_1C84E8 = 7; D_801C78EA_1C84EA = 0x55;
    D_801C7744_1C8344 = 9; D_801C7740_1C8340 = 0x02000024;
    setup_context_fixture(0x80001000, 0xFFFFFFFF, 2);
    func_8003F23C_3FE3C();
    assert(context_event_count == 6 && context_events[3] == 2 && context_ids[3] == 0x55);
    assert(context_ids[4] == 2 && context_ids[5] == 9 && D_801C78E8_1C84E8 == 2);
    assert(D_80077858_78458 == (s32)0x80003024);
    assert(D_801C78F4_1C84F4 == 1234 && D_801C78F8_1C84F8 == 7);
    context_mode = 0;
}

static void check_numbered_event_start(void) {
    cleanup_checks = 0;
    D_800779A0_785A0[0x66] = 0x08001C3C;
    D_80078608_79208[0x66] = 93;
    D_80077858_78458 = 0;
    trace_count = 0;
    func_8003D310_3DF10(0x66);
    assert(trace_count == 1 && trace[0] == RESET);
    assert(reset_args[0] == 0x08001C3C && reset_args[1] == 93);
    assert(D_801C7900_1C8500 == 3 && D_801C7904_1C8504 == -1);

    D_800779A0_785A0[3] = 0x08001234;
    D_80078608_79208[3] = -1;
    D_80077858_78458 = 0x1234;
    trace_count = 0;
    func_8003D310_3DF10(3);
    assert(trace_count == 3 && trace[0] == RESET && trace[1] == CLEANUP && trace[2] == RESET);
    assert(reset_args[0] == 0x08001234 && reset_args[1] == -1);
    assert(D_801C7900_1C8500 == 3 && D_801C7904_1C8504 == -1);
    D_80077858_78458 = 0;
}

static void check_context_event_start(void) {
    static u8 owner[0x64];
    cleanup_checks = 0;
    D_800779A0_785A0[0x66] = 0x08001C3C;
    D_80078608_79208[0x66] = 93;
    owner[0x60] = 0xE1;
    D_801FC600_5B8510[1] = owner;
    D_80077858_78458 = 0;
    trace_count = 0;
    func_8003D388_3DF88(0x66, 1);
    assert(trace_count == 1 && trace[0] == RESET);
    assert(D_801C7900_1C8500 == 1 && D_801C7904_1C8504 == 0xE1);
    assert(reset_args[0] == 0x08001C3C && reset_args[1] == 93);
    assert(owner[0x60] == 0xE1);

    D_801FC600_5B8510[2] = NULL;
    D_80077858_78458 = 1;
    trace_count = 0;
    func_8003D388_3DF88(0x66, 2);
    assert(trace_count == 3 && trace[0] == RESET && trace[1] == CLEANUP && trace[2] == RESET);
    assert(D_801C7900_1C8500 == 2 && D_801C7904_1C8504 == -1);
    assert(reset_args[0] == 0x08001C3C && reset_args[1] == 93);
    D_80077858_78458 = 0;
}

static void check_controller_context_routing(void) {
    CONTROLLER_W before;
    CONTROLLER_W *first = &D_8015C5C8_15D1C8->controller[0];
    CONTROLLER_W *second = &D_8015C5C8_15D1C8->controller[1];
    _Static_assert(sizeof(CONTROLLER_W) == 24, "controller size");
    _Static_assert(offsetof(SYS_W, controller) == 0x3B078, "controller system offset");
    _Static_assert(offsetof(CONTROLLER_W, stick_x) == 0xC, "float axis offset");
    memset(first, 0, sizeof(*first)); memset(second, 0, sizeof(*second));
    first->status = 1; first->button_held_down = 0x1000; first->button_pressed = 0x2000;
    first->stick_raw_x = 100; first->stick_raw_y = -100;
    first->stick_x = 1.25f; first->stick_y = -2.5f; first->stick_magnitude = 3.75f;
    second->status = 2; second->button_held_down = 0x0400; second->button_pressed = 0x0080;
    second->stick_raw_x = 50; second->stick_raw_y = -60;
    second->stick_x = 4.25f; second->stick_y = -5.5f; second->stick_magnitude = 6.75f;
    D_801C7900_1C8500 = 1; func_8003D17C_3DD7C();
    assert(D_801C7908_1C8508.status == 1 && D_801C7908_1C8508.button_pressed == 0x2000);
    assert(D_801C7908_1C8508.stick_raw_x == 100 && D_801C7908_1C8508.stick_y == -2.5f);
    D_801C7900_1C8500 = 2; func_8003D17C_3DD7C();
    assert(D_801C7908_1C8508.status == 2 && D_801C7908_1C8508.button_pressed == 0x0080);
    assert(D_801C7908_1C8508.stick_raw_y == -60 && D_801C7908_1C8508.stick_magnitude == 6.75f);
    ((u8 *)&D_801C7908_1C8508)[0xA] = 0xA5;
    ((u8 *)&D_801C7908_1C8508)[0xB] = 0x5A;
    D_801C7900_1C8500 = 3; func_8003D17C_3DD7C();
    assert(D_801C7908_1C8508.status == 3 && D_801C7908_1C8508.button_held_down == 0x1400);
    assert(D_801C7908_1C8508.button_pressed == 0x2080);
    assert(D_801C7908_1C8508.stick_raw_x == 128 && D_801C7908_1C8508.stick_raw_y == -128);
    assert(D_801C7908_1C8508.stick_x == 4.25f && D_801C7908_1C8508.stick_y == -5.5f);
    assert(((u8 *)&D_801C7908_1C8508)[0xA] == 0xA5 && ((u8 *)&D_801C7908_1C8508)[0xB] == 0x5A);
    first->stick_raw_x = 40; second->stick_raw_x = -25;
    first->stick_raw_y = -20; second->stick_raw_y = 30;
    func_8003D17C_3DD7C();
    assert(D_801C7908_1C8508.stick_raw_x == 15 && D_801C7908_1C8508.stick_raw_y == 10);
    memcpy(&before, &D_801C7908_1C8508, sizeof(before));
    D_801C7900_1C8500 = 0; func_8003D17C_3DD7C();
    assert(memcmp(&before, &D_801C7908_1C8508, sizeof(before)) == 0);
    memset(&D_801C7908_1C8508, 0, sizeof(D_801C7908_1C8508));
    memset(first, 0, sizeof(*first)); memset(second, 0, sizeof(*second));
}

static void check_new_vm_dispatch_and_callback(void) {
    VmChoice c={123,-42,0,0,0};
    s32 state, cond, status;
    D_801C7800_1C8400=&c;
    for (state=0;state<5;state++) {
        for (cond=0;cond<3;cond++) {
            for (status=0;status<2;status++) {
                D_801C77E0_1C83E0=state;
                D_801C77F4_1C83F4=cond;
                D_8007785C_7845C=status ? 0x100 : 7;
                dispatch_choice_calls=dispatch_prompt_calls=dispatch_tick_calls=0;
                func_8003EFB0_3FBB0();
                assert(dispatch_choice_calls==(state==2 && cond==1));
                assert(dispatch_prompt_calls==(state==3));
                assert(dispatch_tick_calls==(!status));
                if (dispatch_choice_calls) assert(dispatch_last_x==123 && dispatch_last_y==-42);
            }
        }
    }
    D_801C7740_1C8340=0;
    D_801C7750_1C8350=0;
    trace_count=0;
    func_8003F350_3FF50();
    assert(trace_count==1 && trace[0]==CREATE);
    assert(argument==0 && D_801C7750_1C8350==0x1234);
    D_801C7740_1C8340=0x123456;
    trace_count=0;
    func_8003F350_3FF50();
    assert(trace_count==1 && trace[0]==CREATE);
    assert((uintptr_t)callback==0x123456 && D_801C7750_1C8350==0x1234);
}

int main(void) {
    check_new_vm_dispatch_and_callback(); check_controller_context_routing(); check_numbered_event_start(); check_context_event_start();
    check_choice_index_and_wait_callbacks(); check_resource_context_transitions(); check_choice_directions_and_repeat(); check_choice_navigation_and_confirmation(); check_choice_stream_rendering(); check_prompt_geometry_and_animation(); check_input_gate_and_cleanup(); check_control_queries(); check_resource_address_resolution(); check_operand_callbacks(); check_assignment_operands(); check_comparisons(); check_relocation_and_counters(); check_callbacks_and_dialogue_states();
    puts("VM choices/repeat/streams, inputs, resources, callbacks and dialogue states passed.");
    return 0;
}
