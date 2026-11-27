#include "m2c_types.h"
extern u8 func_80034E8C_35A8C[];
extern u8 func_8021DAEC_5D907C[];
extern M2C_UNK func_08001CF0_6B9A70;

void func_08002F40_6BACC0(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x68) &= ~1;
    ((void (*)(void *, s32, s32, s32))func_8021DAEC_5D907C)(arg0, 0, 0, 0);
    ((void (*)(M2C_UNK *))func_80034E8C_35A8C)(&func_08001CF0_6B9A70);
}
