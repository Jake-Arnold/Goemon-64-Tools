#include "m2c_types.h"
extern M2C_UNK func_80034E8C_35A8C;
extern M2C_UNK func_8021B3BC_5D694C;
extern M2C_UNK func_080042DC_6E2A6C;

void func_08004290_6E2A20(void *arg0, s32 arg1) {
    M2C_FIELD(arg0, s8 *, 0xEC) = 0;
    ((void (*)(void *, s32, f32, s32))&func_8021B3BC_5D694C)(arg0, 1, 0.25f, 2);
    ((void (*)(void *))&func_80034E8C_35A8C)(&func_080042DC_6E2A6C);
}
