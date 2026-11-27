#include "m2c_types.h"
extern u8 func_8003521C_35E1C[];
extern u8 func_8021664C_5D1B1C[];
extern M2C_UNK func_08000E10_6E4DF0;

void func_08000DAC_6E4D8C(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((void (*)(void *, s32, f32, s32))func_8021664C_5D1B1C)(arg0, 0, 1.0f / 3.0f, 1);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x78;
        ((void (*)(M2C_UNK *))func_8003521C_35E1C)(&func_08000E10_6E4DF0);
    }

    *(volatile s32 *)0x80000000 = 1;
}
