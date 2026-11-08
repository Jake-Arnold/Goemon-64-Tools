/* Synthetic VM text-loop control-flow contract. Not in-game or exact-ROM proof. */
#include <assert.h>
#include <stddef.h>
#include <stdio.h>
#include "candidates/vm_text_loop.c"

_Static_assert(offsetof(VmWork, script_word) == 0, "VM first word location");
_Static_assert(offsetof(VmWork, gate_halfword) == 0xA, "VM +0xA halfword location");
_Static_assert(sizeof(VmWork) == 0x14, "VM work record size");
_Static_assert(offsetof(Controller, held) == 2, "controller +2 input");
_Static_assert(offsetof(Controller, pressed) == 4, "controller +4 input");

VmWork D_801C77E8_1C83E8;
s32 D_801C77D8_1C83D8;
s32 D_801C7754_1C8354;
s32 D_801C77E0_1C83E0;
s32 D_801C7770_1C8370;
s32 D_801C7774_1C8374;
s32 D_80077858_78458;
Controller D_801C7908_1C8508;
static s32 steps, handled, resets, state_on_step, bound_on_step, return_null;

s32 func_8003DE80_3EA80(s32 context, s32 script) {
    assert(context == 0x1234);
    ++steps;
    if (state_on_step >= 0) D_801C77E0_1C83E0 = state_on_step;
    if (bound_on_step >= 0) D_801C77D8_1C83D8 = bound_on_step;
    return return_null ? 0 : script + 4;
}
s32 func_8003DE48_3EA48(s32 target) {
    ++handled;
    return target + 123;
}
void func_8003E680_3F280(void) { ++resets; }

static void reset_vm(void) {
    D_801C77E8_1C83E8 = (VmWork){0};
    D_801C77E8_1C83E8.script_word = 0x4000;
    D_801C77E8_1C83E8.gate_halfword = 0;
    D_801C77D8_1C83D8 = 1;
    D_801C7754_1C8354 = 0x1234;
    D_801C77E0_1C83E0 = 1;
    D_801C7770_1C8370 = 0;
    D_801C7774_1C8374 = 7;
    D_80077858_78458 = -1;
    D_801C7908_1C8508 = (Controller){0};
    steps = handled = resets = 0;
    state_on_step = bound_on_step = -1;
    return_null = 0;
}
int main(void) {
    int terminal;
    reset_vm(); D_801C77D8_1C83D8 = 0;
    func_8003DBEC_3E7EC(); assert(steps == 0);

    reset_vm(); D_801C77D8_1C83D8 = -3;
    func_8003DBEC_3E7EC(); assert(steps == 0);

    reset_vm(); D_801C77D8_1C83D8 = 3;
    func_8003DBEC_3E7EC(); assert(steps == 3 && D_801C77E8_1C83E8.script_word == 0x400c);

    reset_vm(); D_801C77D8_1C83D8 = 3; bound_on_step = 1;
    func_8003DBEC_3E7EC(); assert(steps == 1);

    reset_vm(); bound_on_step = 3;
    func_8003DBEC_3E7EC(); assert(steps == 3);

    for (terminal = 3; terminal <= 6; ++terminal) {
        reset_vm(); state_on_step = terminal;
        D_801C77E8_1C83E8.gate_halfword = 9;
        func_8003DBEC_3E7EC();
        assert(steps == 1 && D_801C77E8_1C83E8.gate_halfword == 0);
        assert(D_801C77E0_1C83E0 == terminal);
    }

    reset_vm(); return_null = 1;
    func_8003DBEC_3E7EC();
    assert(steps == 1 && D_801C77E0_1C83E0 == 0);

    reset_vm(); D_801C7770_1C8370 = 1;
    D_801C77D8_1C83D8 = 2;
    D_801C77E8_1C83E8.gate_halfword = 9;
    D_801C7908_1C8508.pressed = 0xC000;
    func_8003DBEC_3E7EC();
    assert(steps == 2 && handled == 0 && D_801C77E8_1C83E8.gate_halfword == 9);

    reset_vm(); D_801C7774_1C8374 = 0;
    D_801C77E8_1C83E8.gate_halfword = 9;
    D_801C7908_1C8508.pressed = 0x4000;
    func_8003DBEC_3E7EC();
    assert(steps == 1 && resets == 1 && handled == 0 && D_801C77E8_1C83E8.gate_halfword == 0);

    reset_vm(); D_801C7908_1C8508.pressed = 0x4000;
    func_8003DBEC_3E7EC();
    assert(steps == 1 && handled == 1 && resets == 0 && D_80077858_78458 == 130);
    assert(D_801C77E0_1C83E0 == 0);

    reset_vm(); D_801C77E8_1C83E8.gate_halfword = 1;
    D_801C7908_1C8508.held = 0x8000;
    func_8003DBEC_3E7EC();
    assert(steps == 4 && D_801C77E8_1C83E8.gate_halfword == 1);

    reset_vm(); D_801C77E8_1C83E8.gate_halfword = 1;
    D_801C7908_1C8508.pressed = 0x8000;
    func_8003DBEC_3E7EC();
    assert(steps == 1 && D_801C77E8_1C83E8.gate_halfword == 0);

    reset_vm(); D_801C7908_1C8508.held = 0x8000;
    func_8003DBEC_3E7EC();
    assert(steps == 1 && D_801C77E8_1C83E8.gate_halfword == 0);

    reset_vm(); D_801C7908_1C8508.pressed = 0x8000;
    func_8003DBEC_3E7EC();
    assert(steps == 2 && D_801C77E8_1C83E8.gate_halfword == 0);

    reset_vm(); D_801C7908_1C8508.pressed = 0xC000;
    func_8003DBEC_3E7EC();
    assert(steps == 4 && handled == 4 && D_80077858_78458 == 130);

    puts("VM text-loop: 15 scenario groups passed (synthetic host semantics only)");
    return 0;
}
