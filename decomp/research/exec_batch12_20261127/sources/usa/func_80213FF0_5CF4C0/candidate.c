#include "m2c_types.h"

extern u8 func_80038B98_39798[];
extern u8 func_801DCD48_598C58[];
extern u8 func_8021804C_5D351C[];

void func_80213FF0_5CF4C0(void *arg0, M2C_UNK arg1) {
    ((void (*)(s32))func_80038B98_39798)(0x26C);
    ((void (*)(s32))func_801DCD48_598C58)(2);
    ((void (*)(void *, s32))func_8021804C_5D351C)(arg0, 0);
    M2C_FIELD(arg0, s32 *, 0x68) |= 2;
}
