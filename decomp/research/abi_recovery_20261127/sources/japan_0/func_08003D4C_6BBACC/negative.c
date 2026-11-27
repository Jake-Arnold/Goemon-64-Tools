#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021BB68_5D70F8;
extern char func_8021DB00_5D9090;
extern M2C_UNK func_08003E08_6BBB88;

void func_08003D4C_6BBACC(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s16 *, 0x5E) = 0xCB;
    M2C_FIELD(arg0, s32 *, 0x60) = 0x2006E1;
    ((M2C_UNK  (*)(void *, M2C_UNK))&func_8021BB68_5D70F8)(arg0, 6);
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK, s32))&func_8021DB00_5D9090)(arg0, 0x32, 0x32, 0xA, 0);
    M2C_FIELD(arg1, f32 *, 0x24) = 1.0f;
    M2C_FIELD(arg1, f32 *, 0x20) = 1.0f;
    M2C_FIELD(arg1, f32 *, 0x1C) = 1.0f;
    M2C_FIELD(arg0, s8 *, 0x4C) = 0;
    M2C_FIELD(arg1, f32 *, 8) = 0.0f;
    M2C_FIELD(arg1, f32 *, 0x10) = 0.0f;
    M2C_FIELD(arg1, f32 *, 0xC) = -186.0f;
    M2C_FIELD(arg0, s16 *, 0x8A) = 0x32;
    ((M2C_UNK (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_08003E08_6BBB88);

    *(volatile s32 *)0x80000000 = 1;
}
