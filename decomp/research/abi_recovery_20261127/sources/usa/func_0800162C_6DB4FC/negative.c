#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021BB04_5D6FD4;
extern M2C_UNK func_080014A0_6DB370;

void func_0800162C_6DB4FC(void *arg0, M2C_UNK arg1) {
    if (((s32  (*)(void *, s32, s32, M2C_UNK))&func_8021BB04_5D6FD4)(arg0, M2C_FIELD(arg0, s32 *, 0xDC), M2C_FIELD(arg0, s32 *, 0xE0), 0x3F800000) == 0) {
        M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
        ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_080014A0_6DB370);
    }

    *(volatile s32 *)0x80000000 = 1;
}
