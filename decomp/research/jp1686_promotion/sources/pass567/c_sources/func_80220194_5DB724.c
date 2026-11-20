#include "../m2c_types.h"
f32 func_80003D40_4940(s32);                        /* extern */
f32 func_80003DD0_49D0(u16);                        /* extern */

void func_80220194_5DB724(void *arg0, u16 arg1, f32 arg2) {
    M2C_FIELD(arg0, u16 *, 0x88) = arg1;
    M2C_FIELD(arg0, f32 *, 0x78) = (f32) (func_80003D40_4940(arg1 & 0xFFFF) * arg2);
    M2C_FIELD(arg0, f32 *, 0x80) = (f32) (func_80003DD0_49D0(arg1) * arg2);
}
