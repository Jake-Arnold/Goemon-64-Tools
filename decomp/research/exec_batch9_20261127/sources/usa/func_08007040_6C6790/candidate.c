#include "m2c_types.h"
extern M2C_UNK func_8003521C_35E1C;
extern M2C_UNK func_8021664C_5D1B1C;
extern M2C_UNK func_08007094_6C67E4;

void func_08007040_6C6790(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((void (*)(void *, s32, s32, s32))&func_8021664C_5D1B1C)(arg0, 2, 0x3D088889, 0);
        ((void (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08007094_6C67E4);
    }
}
