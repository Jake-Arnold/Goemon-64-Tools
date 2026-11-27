#include "m2c_types.h"
extern M2C_UNK func_80034E8C_35A8C;
extern M2C_UNK func_080008D4_7000A4;

void func_0800091C_7000EC(void *arg0, s32 arg1) {
    if (--M2C_FIELD(arg0, u16 *, 0x8A) == 0) {
        M2C_FIELD(arg0, u16 *, 0x8A) = 0x32;
        M2C_FIELD(arg0, f32 *, 0x80) = -0.5f;
        M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
        ((void (*)(void *))&func_80034E8C_35A8C)(&func_080008D4_7000A4);
    }

    *(volatile s32 *)0x80000000 = 1;
}
