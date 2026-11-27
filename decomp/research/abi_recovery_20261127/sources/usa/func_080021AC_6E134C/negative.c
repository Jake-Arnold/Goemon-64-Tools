#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80216FFC_5D24CC;
extern char func_80218D7C_5D424C;
extern char func_80218D90_5D4260;
extern char func_80218DA8_5D4278;
extern M2C_UNK func_0800229C_6E143C;

void func_080021AC_6E134C(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s32 *, 0x60) = 0x2416C1;
    ((M2C_UNK  (*)(void *, M2C_UNK, M2C_UNK))&func_80216FFC_5D24CC)(arg0, 0x190, 0);
    M2C_FIELD(arg1, f32 *, 0x24) = 1.0f;
    M2C_FIELD(arg1, f32 *, 0x20) = 1.0f;
    M2C_FIELD(arg1, f32 *, 0x1C) = 1.0f;
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_80218D7C_5D424C)(arg0, 0, 0, 0);
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_80218DA8_5D4278)(arg0, 0xE, 0, 0);
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK, s32))&func_80218D90_5D4260)(arg0, 0x14, 0xA, 0xA, 0);
    M2C_FIELD(arg0, s8 *, 0x4C) = 0;
    M2C_FIELD(arg0, s16 *, 0x8A) = (s16) ((M2C_FIELD(arg0, s32 *, 0xD0) << 6) + 1);
    M2C_FIELD(arg0, s8 *, 0x8E) = 1;
    M2C_FIELD(arg0, s8 *, 0x8F) = 2;
    ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_0800229C_6E143C);

    *(volatile s32 *)0x80000000 = 1;
}
