#include "common.h"
void func_80016660_17260(s32 arg0, s32 arg1) {
    u8 *temp_v0;
    temp_v0 = (arg1 >> 3) + arg0;
    *temp_v0 |= 1 << (arg1 & 7);
}
void func_80016684_17284(s32 arg0, s32 arg1) {
    u8 *temp_v0;
    temp_v0 = (arg1 >> 3) + arg0;
    *temp_v0 &= ~(1 << (arg1 & 7));
}
#pragma GLOBAL_ASM("asm/usa/nonmatchings/bit_array/func_800166AC_172AC.s")
