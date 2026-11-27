#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021BD6C_5D72FC;
extern char func_8021DAEC_5D907C;
extern char func_8021DB00_5D9090;
extern char func_8021DB18_5D90A8;
extern M2C_UNK func_0800229C_6E5C0C;

void func_080021AC_6E5B1C(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s32 *, 0x60) = 0x2416C1;
    ((M2C_UNK  (*)(void *, M2C_UNK, M2C_UNK))&func_8021BD6C_5D72FC)(arg0, 0x190, 0);
    M2C_FIELD(arg1, f32 *, 0x24) = 1.0f;
    M2C_FIELD(arg1, f32 *, 0x20) = 1.0f;
    M2C_FIELD(arg1, f32 *, 0x1C) = 1.0f;
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8021DAEC_5D907C)(arg0, 0, 0, 0);
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8021DB18_5D90A8)(arg0, 0xE, 0, 0);
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK, s32))&func_8021DB00_5D9090)(arg0, 0x14, 0xA, 0xA, 0);
    M2C_FIELD(arg0, s8 *, 0x4C) = 0;
    M2C_FIELD(arg0, s16 *, 0x8A) = (s16) ((M2C_FIELD(arg0, s32 *, 0xD0) << 6) + 1);
    M2C_FIELD(arg0, s8 *, 0x8E) = 1;
    M2C_FIELD(arg0, s8 *, 0x8F) = 2;
    ((M2C_UNK (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_0800229C_6E5C0C);
}
