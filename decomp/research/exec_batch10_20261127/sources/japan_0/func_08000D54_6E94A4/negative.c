#include "m2c_types.h"
extern u8 func_80034E8C_35A8C[];
extern u8 func_8021B3BC_5D694C[];
extern M2C_UNK func_08000DB8_6E9508;

void func_08000D54_6E94A4(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((void (*)(void *, s32, f32, s32))func_8021B3BC_5D694C)(arg0, 0, 1.0f / 3.0f, 1);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x78;
        ((void (*)(M2C_UNK *))func_80034E8C_35A8C)(&func_08000DB8_6E9508);
    }

    *(volatile s32 *)0x80000000 = 1;
}
