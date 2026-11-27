#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80216DF8_5D22C8;
extern char func_80218D90_5D4260;
extern M2C_UNK func_08003E6C_6B710C;

void func_08003DB0_6B7050(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s16 *, 0x5E) = 0xCB;
    M2C_FIELD(arg0, s32 *, 0x60) = 0x2006E1;
    ((M2C_UNK  (*)(void *, M2C_UNK))&func_80216DF8_5D22C8)(arg0, 6);
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK, s32))&func_80218D90_5D4260)(arg0, 0x32, 0x32, 0xA, 0);
    M2C_FIELD(arg1, f32 *, 0x24) = 1.0f;
    M2C_FIELD(arg1, f32 *, 0x20) = 1.0f;
    M2C_FIELD(arg1, f32 *, 0x1C) = 1.0f;
    M2C_FIELD(arg0, s8 *, 0x4C) = 0;
    M2C_FIELD(arg1, f32 *, 8) = 0.0f;
    M2C_FIELD(arg1, f32 *, 0x10) = 0.0f;
    M2C_FIELD(arg1, f32 *, 0xC) = -186.0f;
    M2C_FIELD(arg0, s16 *, 0x8A) = 0x32;
    ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08003E6C_6B710C);
}
