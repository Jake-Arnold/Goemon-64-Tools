#include "m2c_types.h"

extern u8 func_80038808_39408[];
extern u8 func_801E2130_59E100[];
extern u8 func_8021CDBC_5D834C[];

void func_80219388_5D4918(void *arg0, M2C_UNK arg1) {
    ((void (*)(s32))func_80038808_39408)(0x26B);
    ((void (*)(s32))func_801E2130_59E100)(5);
    ((void (*)(void *, s32))func_8021CDBC_5D834C)(arg0, 0);
    M2C_FIELD(arg0, s32 *, 0x68) |= 2;

    *(volatile int *)0x80000000 = 1;
}
