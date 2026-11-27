#include "m2c_types.h"

extern u8 func_8021B3BC_5D694C[];
extern u8 func_8021DAEC_5D907C[];
extern u8 func_80034E8C_35A8C[];
extern u8 func_080011A0_6ECBD0[];

void func_08001128_6ECB58(void *arg0, void *arg1) {
    ((void (*)(void *, s32, s32, s32))func_8021B3BC_5D694C)(arg0, 1, 0x3EAAAAAB, 0);
    ((void (*)(void *, s32, s32, s32))func_8021DAEC_5D907C)(arg0, 0x28, 0x50, 0);
    *(s16 *)((u8 *)arg0 + 0x8A) = 0x14;
    ((void (*)(void *))func_80034E8C_35A8C)(func_080011A0_6ECBD0);
}
