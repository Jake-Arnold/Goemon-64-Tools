#include "m2c_types.h"

extern u8 func_80034E8C_35A8C[];
extern u8 func_8021B3BC_5D694C[];
extern u8 func_08000898_6E8FE8[];

void func_08000838_6E8F88(void *arg0, s32 arg1) {
    ((void (*)(void *, s32, s32, s32))func_8021B3BC_5D694C)(arg0, 0, 0x3EAAAAAB, 1);
    M2C_FIELD(arg0, s32 *, 0x60) = 0x2016E1;
    ((void (*)(void *))func_80034E8C_35A8C)(func_08000898_6E8FE8);
}
