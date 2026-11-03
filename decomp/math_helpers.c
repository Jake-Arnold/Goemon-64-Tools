#include "common.h"
s32 func_800040A8_4CA8(f32, f32);
f32 func_80003E10_4A10(u16);
f32 func_80003EA0_4AA0(u16);
s32 func_8000E28C_EE8C(f32 a, f32 b, f32 c, f32 d) { unsigned short v; return (v = func_800040A8_4CA8(b - d, a - c)) & 0x3FF; }
#pragma GLOBAL_ASM("asm/usa/nonmatchings/math_helpers/func_8000E2D4_EED4.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/math_helpers/func_8000E39C_EF9C.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/math_helpers/func_8000E4E4_F0E4.s")
s32 func_8000E630_F230(f32 arg0, u16 arg1, f32 *arg2, f32 *arg3) {
    *arg2 = func_80003EA0_4AA0(arg1) * arg0;
    *arg3 = func_80003E10_4A10(arg1) * arg0;
    return 1;
}
