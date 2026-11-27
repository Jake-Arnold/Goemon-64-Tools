#include "m2c_types.h"

extern u8 func_80038808_39408[];
extern u8 func_801E2188_59E158[];
extern u8 func_8021CDBC_5D834C[];

void func_80218D88_5D4318(void *arg0, M2C_UNK arg1) {
    ((void (*)(s32))func_80038808_39408)(0x26C);
    ((void (*)(s32))func_801E2188_59E158)(2);
    ((void (*)(void *, s32))func_8021CDBC_5D834C)(arg0, 0);
    M2C_FIELD(arg0, s32 *, 0x68) |= 2;
}
