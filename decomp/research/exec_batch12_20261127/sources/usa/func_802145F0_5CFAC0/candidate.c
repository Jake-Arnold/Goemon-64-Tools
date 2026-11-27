#include "m2c_types.h"

extern u8 func_80038B98_39798[];
extern u8 func_801DCCF0_598C00[];
extern u8 func_8021804C_5D351C[];

void func_802145F0_5CFAC0(void *arg0, M2C_UNK arg1) {
    ((void (*)(s32))func_80038B98_39798)(0x26B);
    ((void (*)(s32))func_801DCCF0_598C00)(5);
    ((void (*)(void *, s32))func_8021804C_5D351C)(arg0, 0);
    M2C_FIELD(arg0, s32 *, 0x68) |= 2;
}
