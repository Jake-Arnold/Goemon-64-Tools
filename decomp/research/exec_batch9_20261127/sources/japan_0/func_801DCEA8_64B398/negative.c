#include "m2c_types.h"
extern f64 D_801F4920_662E10;

void func_801DCEA8_64B398(void *arg0, u8 arg1) {
    s32 temp = M2C_FIELD(arg0, s32 *, 0xA0);

    M2C_FIELD(arg0, s8 *, 0x9C) = (arg1 != 0) + 3;
    temp = (temp < 0) * 2 - 1;
    M2C_FIELD(arg0, s32 *, 0xA4) = (s32) (temp * D_801F4920_662E10);

    *(volatile s32 *)0x80000000 = 1;
}
