#include "m2c_types.h"
extern u8 func_80034E8C_35A8C[];
extern u8 func_8021B3BC_5D694C[];
extern M2C_UNK func_08003D28_6E24B8;

void func_08003EF8_6E2688(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((void (*)(void *, s32, s32, s32))func_8021B3BC_5D694C)(arg0, 1, 0x3E800000, 4);
        ((void (*)(M2C_UNK *))func_80034E8C_35A8C)(&func_08003D28_6E24B8);
    }
}
