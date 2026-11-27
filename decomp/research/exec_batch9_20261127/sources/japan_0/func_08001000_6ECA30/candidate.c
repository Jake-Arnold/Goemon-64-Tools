#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);
M2C_UNK func_8021B3BC_5D694C(void *, s32, f32, s32);
extern M2C_UNK func_08001054_6ECA84;

void func_08001000_6ECA30(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((void (*)(void *, s32, f32, s32))func_8021B3BC_5D694C)(arg0, 0, 1.0f / 3.0f, 1);
        ((void (*)(M2C_UNK *))func_80034E8C_35A8C)(&func_08001054_6ECA84);
    }
}
