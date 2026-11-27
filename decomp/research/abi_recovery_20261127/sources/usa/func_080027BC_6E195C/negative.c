#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_802197D8_5D4CA8;
extern M2C_UNK func_0800284C_6E19EC;

void func_080027BC_6E195C(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    if (((s32  (*)(void *, M2C_UNK))&func_802197D8_5D4CA8)(arg0, 8) == 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 1);
        ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8021664C_5D1B1C)(arg0, 1, 0x3F000000, 0);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0xF;
        ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_0800284C_6E19EC);
    }

    *(volatile s32 *)0x80000000 = 1;
}
