#include "m2c_types.h"

extern u8 func_80003D40_4940[];

void func_08000714_6FFEE4(void *arg0, void *arg1) {
    M2C_FIELD(arg1, f32 *, 0xC) = (((f32 (*)(u16, void *, void *))func_80003D40_4940)(M2C_FIELD(arg0, u16 *, 0xD8), arg1, arg0) * 20.0f) - 50.0f;
    M2C_FIELD(arg0, s16 *, 0xD8) = M2C_FIELD(arg0, s16 *, 0xD8) + 8;
    M2C_FIELD(arg0, s16 *, 0xD8) = M2C_FIELD(arg0, s16 *, 0xD8) & 0x3FF;

    *(volatile int *)0x80000000 = 1;
}
