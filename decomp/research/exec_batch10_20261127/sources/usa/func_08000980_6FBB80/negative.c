#include "m2c_types.h"
extern M2C_UNK func_8003521C_35E1C(void *);
extern M2C_UNK func_0800091C_6FBB1C;

void func_08000980_6FBB80(void *arg0, M2C_UNK arg1) {
    if (--M2C_FIELD(arg0, u16 *, 0x8A) == 0) {
        M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x7C) = -0.5f;
        M2C_FIELD(arg0, u16 *, 0x8A) = 0x5AU;
        ((void (*)(void *))func_8003521C_35E1C)(&func_0800091C_6FBB1C);
    }

    *(volatile s32 *)0x80000000 = 1;
}
