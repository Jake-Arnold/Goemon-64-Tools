#include "m2c_types.h"

extern u8 func_8021664C_5D1B1C[];
extern u8 func_80218D7C_5D424C[];
extern u8 func_8003521C_35E1C[];
extern u8 func_080011A4_6E84B4[];

void func_0800112C_6E843C(void *arg0, void *arg1) {
    ((void (*)(void *, s32, s32, s32))func_8021664C_5D1B1C)(arg0, 1, 0x3EAAAAAB, 0);
    ((void (*)(void *, s32, s32, s32))func_80218D7C_5D424C)(arg0, 0x28, 0x50, 0);
    *(s16 *)((u8 *)arg0 + 0x8A) = 0x14;
    ((void (*)(void *))func_8003521C_35E1C)(func_080011A4_6E84B4);
}
