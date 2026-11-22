#include "m2c_types.h"
f32 _nsqrtf(f32);                                   /* extern */
s16 func_80003FD8_4BD8(f32, f32);                   /* extern */

void func_8000E9C4_F5C4(f32 arg0, f32 arg1, f32 arg2, f32 arg3, f32 arg4, f32 arg5, s16 *arg6, s16 *arg7) {
    f32 sp1C;
    f32 sp18;
    f32 temp_f0;
    f32 temp_f0_2;
    f32 temp_f2;
    f32 var_f14;

    temp_f0 = arg0 - arg3;
    temp_f2 = arg2 - arg5;
    sp1C = temp_f0;
    sp18 = temp_f2;
    temp_f0_2 = _nsqrtf((temp_f0 * temp_f0) + (temp_f2 * temp_f2));
    if (temp_f0_2 < 0.0f) {
        var_f14 = -temp_f0_2;
    } else {
        var_f14 = temp_f0_2;
    }
    *arg6 = (0x400 - func_80003FD8_4BD8(arg1 - arg4, var_f14)) & 0x3FF;
    *arg7 = func_80003FD8_4BD8(sp1C, sp18);
}
