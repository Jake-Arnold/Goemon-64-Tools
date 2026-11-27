#include "m2c_types.h"
extern M2C_UNK func_80034E8C_35A8C;
extern M2C_UNK func_8021B3BC_5D694C;
extern M2C_UNK func_08004518_6E2CA8;

void func_080044CC_6E2C5C(void *arg0, s32 arg1) {
    M2C_FIELD(arg0, s8 *, 0xEC) = 0;
    ((void (*)(void *, s32, f32, s32))&func_8021B3BC_5D694C)(arg0, 0, 0.5f, 2);
    ((void (*)(void *))&func_80034E8C_35A8C)(&func_08004518_6E2CA8);
}
