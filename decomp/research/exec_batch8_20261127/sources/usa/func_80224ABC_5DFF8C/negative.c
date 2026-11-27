#include "m2c_types.h"
void func_80224560_5DFA30(u8 *, s32, f32, s32, u8 *, u8 *, u8 *, s32);

void func_80224ABC_5DFF8C(u8 *arg0, s32 arg1, f32 arg2, s32 arg3) {
    func_80224560_5DFA30(arg0, arg1, arg2, arg3, arg0 + 0xAE, arg0 + 0xAD, arg0 + 0xAC, 3);

    *(volatile s32 *)0x80000000 = 1;
}
