#include "m2c_types.h"
void func_80034E8C_35A8C(M2C_UNK *);
void func_8021B3BC_5D694C(void *, s32, s32, s32);
extern M2C_UNK func_08001600_6C57C0;

void func_08001594_6C5754(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, u16 *, 0x8A)--) {
        return;
    }
    M2C_FIELD(arg0, s32 *, 0x60) |= 0x01000000;
    ((void (*)(void *, s32, s32, s32))func_8021B3BC_5D694C)(arg0, 1, 0x3D088889, 0);
    ((void (*)(M2C_UNK *))func_80034E8C_35A8C)(&func_08001600_6C57C0);
}
