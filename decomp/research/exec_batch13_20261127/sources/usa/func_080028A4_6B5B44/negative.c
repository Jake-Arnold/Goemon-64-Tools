#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_8021664C_5D1B1C[];
extern u8 func_80218D7C_5D424C[];
extern s8 D_8015CDB4;
extern u8 func_08002918_6B5BB8[];

void func_080028A4_6B5B44(s32 arg0, s32 arg1) {
    ((void (*)(s32, s32, u32, s32))func_8021664C_5D1B1C)(arg0, 1, 0x3EAAAAAB, 1);
    ((void (*)(s32, s32, s32, s32))func_80218D7C_5D424C)(arg0, 0x190, 0x190, 0xC8);
    D_8015CDB4 = 0;
    ((void (*)(void *))func_8003521C_35E1C)(func_08002918_6B5BB8);

    *(volatile int *)0x80000000 = 1;
}
