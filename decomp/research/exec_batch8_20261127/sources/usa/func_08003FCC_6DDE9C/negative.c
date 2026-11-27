#include "m2c_types.h"
extern u8 func_8003521C_35E1C[];
extern u8 func_8021664C_5D1B1C[];
extern M2C_UNK func_08003DFC_6DDCCC;

void func_08003FCC_6DDE9C(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((void (*)(void *, s32, s32, s32))func_8021664C_5D1B1C)(arg0, 1, 0x3E800000, 4);
        ((void (*)(M2C_UNK *))func_8003521C_35E1C)(&func_08003DFC_6DDCCC);
    }

    *(volatile s32 *)0x80000000 = 1;
}
