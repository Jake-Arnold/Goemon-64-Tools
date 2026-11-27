#include "m2c_types.h"
extern M2C_UNK func_80034E8C_35A8C;
extern M2C_UNK func_8021B3BC_5D694C;
extern M2C_UNK func_08007094_6CB254;

void func_08007040_6CB200(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((void (*)(void *, s32, s32, s32))&func_8021B3BC_5D694C)(arg0, 2, 0x3D088889, 0);
        ((void (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_08007094_6CB254);
    }

    *(volatile s32 *)0x80000000 = 1;
}
