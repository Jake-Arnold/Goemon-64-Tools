#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80216DF8_5D22C8;
extern char func_80218D90_5D4260;
extern char func_80219E70_5D5340;
extern M2C_UNK func_08006C18_6C6368;

void func_08006B40_6C6290(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x1C1;
    M2C_FIELD(arg0, s32 *, 0x60) = 0x8EA007E1;
    ((M2C_UNK  (*)(void *, M2C_UNK))&func_80216DF8_5D22C8)(arg0, 0);
    M2C_FIELD(arg0, s8 *, 0x6C) = 0;
    M2C_FIELD(arg0, s16 *, 0x96) = 0x1E1;
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK, s32))&func_80218D90_5D4260)(arg0, 0x14, 0x14, 0xA, 0);
    M2C_FIELD(arg1, f32 *, 8) = 170.0f;
    M2C_FIELD(arg1, f32 *, 0xC) = -100.0f;
    M2C_FIELD(arg1, f32 *, 0x10) = 135.0f;
    M2C_FIELD(arg0, s16 *, 0xDC) = 0;
    M2C_FIELD(arg0, f32 *, 0xD0) = (f32) M2C_FIELD(arg0, f32 *, 0x78);
    M2C_FIELD(arg0, f32 *, 0xD4) = (f32) M2C_FIELD(arg0, f32 *, 0x80);
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK))&func_80219E70_5D5340)(arg0, 5, 0);
    ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08006C18_6C6368);
}
