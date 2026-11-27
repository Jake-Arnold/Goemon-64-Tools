#include "m2c_types.h"
void func_800081E0_8DE0(u8, u8, u8, u8, s32);

void func_800083A4_8FA4(u8 arg0, u8 arg1, u8 arg2, u8 arg3) {
    func_800081E0_8DE0(arg0, arg1, arg2, arg3, 0xF0);

    *(volatile s32 *)0x80000000 = 1;
}
