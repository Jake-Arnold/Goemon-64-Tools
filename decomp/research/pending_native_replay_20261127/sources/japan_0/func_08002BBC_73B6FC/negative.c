#include "m2c_types.h"
extern char func_80034E84_35A84;
extern char func_80034E8C_35A8C;
extern char func_80034EB4_35AB4;
extern char func_8021BB8C_5D711C;
extern char func_8022982C_5E4DBC;
extern M2C_UNK D_80162420_163020;
extern M2C_UNK func_08002C98_73B7D8;
extern M2C_UNK func_8021DCA0_5D9230;
extern M2C_UNK func_8021DFCC_5D955C;

void func_08002BBC_73B6FC(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s32 *, 0x60) = 0x20;
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x359;
    ((M2C_UNK  (*)(void *, M2C_UNK))&func_8021BB8C_5D711C)(arg0, 0);
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8022982C_5E4DBC)(arg0, 0, 0x40400000, 1);
    M2C_FIELD(arg1, f32 *, 0x24) = 1.0f;
    M2C_FIELD(arg1, f32 *, 0x20) = 1.0f;
    M2C_FIELD(arg1, f32 *, 0x1C) = 1.0f;
    ((M2C_UNK (*)(void *, M2C_UNK *))&func_80034E84_35A84)(arg0, &func_8021DFCC_5D955C);
    ((M2C_UNK (*)(void *, M2C_UNK *))&func_80034EB4_35AB4)(arg0, &func_8021DCA0_5D9230);
    M2C_FIELD(arg0, u8 *, 0x74) = (u8) M2C_FIELD(&D_80162420_163020, u8 *, 0xD8);
    M2C_FIELD(&D_80162420_163020, u8 *, 0xD8) = (u8) (M2C_FIELD(&D_80162420_163020, u8 *, 0xD8) + 1);
    ((M2C_UNK (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_08002C98_73B7D8);

    *(volatile s32 *)0x80000000 = 1;
}
