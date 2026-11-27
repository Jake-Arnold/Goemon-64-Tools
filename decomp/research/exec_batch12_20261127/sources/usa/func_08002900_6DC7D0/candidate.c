#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_8021664C_5D1B1C[];
extern u8 func_80218DCC_5D429C[];
extern u8 func_0800296C_6DC83C[];

void func_08002900_6DC7D0(void *arg0, s32 arg1) {
    ((void (*)(void *, s32, f32, s32))func_8021664C_5D1B1C)(arg0, 0, 0.5f, 1);
    ((void (*)(void *, s32))func_80218DCC_5D429C)(arg0, 1);
    *(s8 *)((u8 *)arg0 + 0xD9) = 0xA;
    ((void (*)(void *))func_8003521C_35E1C)(func_0800296C_6DC83C);
}
