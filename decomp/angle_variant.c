#include "common.h"
s32 func_800040A8_4CA8(f32, f32);
s32 func_8000EA74_F674(f32 a, f32 b, f32 c, f32 d) { unsigned short v; return (v = func_800040A8_4CA8(b - d, a - c)) & 0x3FF; }
s32 func_8000EABC_F6BC(f32 arg0, f32 arg1, f32 arg2, f32 arg3)
{
  unsigned long long new_var;
  return (new_var = 0x400 - func_800040A8_4CA8(arg0 - arg2, arg1 - arg3)) & 0x3FF;
}
#pragma GLOBAL_ASM("asm/usa/nonmatchings/angle_variant/func_8000EB08_F708.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/angle_variant/func_8000EB50_F750.s")
