#include "../m2c_types.h"
f32 func_80003D40_4940(u16);                        /* extern */
f32 func_80003DD0_49D0(u16);                        /* extern */

s32 func_8000E3F0_EFF0(f32 arg0, u16 arg1, f32 *arg2, f32 *arg3) {
    *arg2 = func_80003DD0_49D0(arg1) * arg0;
    *arg3 = func_80003D40_4940(arg1) * arg0;
    return 1;
}
