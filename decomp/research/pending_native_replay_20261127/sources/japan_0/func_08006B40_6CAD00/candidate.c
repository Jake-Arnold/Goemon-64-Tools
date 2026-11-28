#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021BB68_5D70F8;
extern char func_8021DB00_5D9090;
extern char func_8021EBE0_5DA170;
extern M2C_UNK func_08006C18_6CADD8;

void func_08006B40_6CAD00(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x1C1;
    M2C_FIELD(arg0, s32 *, 0x60) = 0x8EA007E1;
    ((M2C_UNK  (*)(void *, M2C_UNK))&func_8021BB68_5D70F8)(arg0, 0);
    M2C_FIELD(arg0, s8 *, 0x6C) = 0;
    M2C_FIELD(arg0, s16 *, 0x96) = 0x1E1;
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK, s32))&func_8021DB00_5D9090)(arg0, 0x14, 0x14, 0xA, 0);
    M2C_FIELD(arg1, f32 *, 8) = 170.0f;
    M2C_FIELD(arg1, f32 *, 0xC) = -100.0f;
    M2C_FIELD(arg1, f32 *, 0x10) = 135.0f;
    M2C_FIELD(arg0, s16 *, 0xDC) = 0;
    M2C_FIELD(arg0, f32 *, 0xD0) = (f32) M2C_FIELD(arg0, f32 *, 0x78);
    M2C_FIELD(arg0, f32 *, 0xD4) = (f32) M2C_FIELD(arg0, f32 *, 0x80);
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK))&func_8021EBE0_5DA170)(arg0, 5, 0);
    ((M2C_UNK (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_08006C18_6CADD8);
}
