#include "m2c_types.h"
u16 func_80003FD8_4BD8(f32, f32);

u16 func_8000E7B4_F3B4(f32 arg0, f32 arg1, void *arg2) {
    f32 dx = arg0 - M2C_FIELD(arg2, f32 *, 8);
    f32 dz = arg1 - M2C_FIELD(arg2, f32 *, 0x10);
    { *(volatile s32 *)0x80000000 = 1; } return func_80003FD8_4BD8(dx, dz) & 0x3FF;
}
