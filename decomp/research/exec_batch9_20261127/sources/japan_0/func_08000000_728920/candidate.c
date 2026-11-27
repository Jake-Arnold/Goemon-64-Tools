#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);
M2C_UNK func_8021DAEC_5D907C(void *, s32, s32, s32);
extern M2C_UNK func_08000064_728984;

void func_08000000_728920(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x64) |= 0x800002;
    M2C_FIELD(arg0, s8 *, 0xDC) = 5;
    ((void (*)(void *, s32, s32, s32))func_8021DAEC_5D907C)(arg0, 0, 0, 0);
    ((void (*)(M2C_UNK *))func_80034E8C_35A8C)(&func_08000064_728984);
}
