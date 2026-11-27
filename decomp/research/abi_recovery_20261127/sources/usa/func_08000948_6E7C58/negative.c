#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_802197D8_5D4CA8;
extern M2C_UNK func_080009CC_6E7CDC;

void func_08000948_6E7C58(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    if (((s32  (*)(void *, M2C_UNK))&func_802197D8_5D4CA8)(arg0, 0x10) == 0) {
        ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8021664C_5D1B1C)(arg0, 1, 0x3E800000, 0);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x14;
        ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_080009CC_6E7CDC);
    }

    *(volatile s32 *)0x80000000 = 1;
}
