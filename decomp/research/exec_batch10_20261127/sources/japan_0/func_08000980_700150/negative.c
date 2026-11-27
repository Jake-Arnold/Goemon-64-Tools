#include "m2c_types.h"
extern M2C_UNK func_80034E8C_35A8C(void *);
extern M2C_UNK func_0800091C_7000EC;

void func_08000980_700150(void *arg0, M2C_UNK arg1) {
    if (--M2C_FIELD(arg0, u16 *, 0x8A) == 0) {
        M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x7C) = -0.5f;
        M2C_FIELD(arg0, u16 *, 0x8A) = 0x5AU;
        ((void (*)(void *))func_80034E8C_35A8C)(&func_0800091C_7000EC);
    }

    *(volatile s32 *)0x80000000 = 1;
}
