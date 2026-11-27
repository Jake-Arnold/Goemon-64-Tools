#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);
M2C_UNK func_8021B3BC_5D694C(void *, s32, f32, s32);
extern M2C_UNK func_08000524_6E3E94;

void func_080004B8_6E3E28(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = temp_v0 - 1;
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, s32 *, 0x60) |= 0x01000001;
        ((void (*)(void *, s32, f32, s32))func_8021B3BC_5D694C)(arg0, 0, 0.25f, 0);
        ((void (*)(M2C_UNK *))func_80034E8C_35A8C)(&func_08000524_6E3E94);
    }
}
