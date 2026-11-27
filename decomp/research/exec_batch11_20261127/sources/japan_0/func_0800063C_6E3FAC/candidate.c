#include "m2c_types.h"
void func_80034E8C_35A8C(void *);
void func_8021B3BC_5D694C(void *, s32, f32, s32);
extern M2C_UNK func_0800069C_6E400C;

void func_0800063C_6E3FAC(void *arg0, M2C_UNK arg1) {
    ((void (*)(void *, s32, f32, s32))func_8021B3BC_5D694C)(arg0, 0, 0.25f, 0);
    M2C_FIELD(arg0, s32 *, 0x60) &= ~1;
    ((void (*)(void *))func_80034E8C_35A8C)(&func_0800069C_6E400C);
}
