#include "m2c_types.h"
f32 func_80003D40_4940(u16);                        /* extern */
f32 func_80003DD0_49D0(u16);                        /* extern */

void func_80223EC4_5DF454(void *arg0, f32 arg1, u16 arg2, u16 arg3) {
    f32 sp1C;

    sp1C = func_80003DD0_49D0(arg2);
    M2C_FIELD(arg0, f32 *, 0x78) = (f32) (func_80003D40_4940(arg3) * sp1C * arg1);
    M2C_FIELD(arg0, f32 *, 0x7C) = (f32) (-func_80003D40_4940(arg2) * arg1);
    sp1C = func_80003DD0_49D0(arg2);
    M2C_FIELD(arg0, f32 *, 0x80) = (f32) (func_80003DD0_49D0(arg3) * sp1C * arg1);
}
