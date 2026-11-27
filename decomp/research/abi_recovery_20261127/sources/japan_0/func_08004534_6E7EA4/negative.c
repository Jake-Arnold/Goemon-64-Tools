#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021E548_5D9AD8;
extern M2C_UNK func_080045A4_6E7F14;

void func_08004534_6E7EA4(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    if (((s32  (*)(void *, M2C_UNK))&func_8021E548_5D9AD8)(arg0, 0x10) == 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 1);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0xF;
        ((M2C_UNK (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_080045A4_6E7F14);
    }

    *(volatile s32 *)0x80000000 = 1;
}
