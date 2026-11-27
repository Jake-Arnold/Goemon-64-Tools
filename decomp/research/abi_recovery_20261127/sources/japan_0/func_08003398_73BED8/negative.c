#include "m2c_types.h"
extern char func_80034E84_35A84;
extern char func_80034E8C_35A8C;
extern char func_80034EB4_35AB4;
extern char func_8021B3BC_5D694C;
extern char func_8021EBE0_5DA170;
extern M2C_UNK D_80162420_163020;
extern M2C_UNK func_08003464_73BFA4;
extern M2C_UNK func_8021DCA0_5D9230;
extern M2C_UNK func_8021DFCC_5D955C;

void func_08003398_73BED8(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x60) = 0x201;
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x351;
    ((M2C_UNK  (*)(void *, M2C_UNK, M2C_UNK))&func_8021EBE0_5DA170)(arg0, 5, 0);
    ((M2C_UNK (*)(void *, M2C_UNK *))&func_80034E84_35A84)(arg0, &func_8021DFCC_5D955C);
    ((M2C_UNK (*)(void *, M2C_UNK *))&func_80034EB4_35AB4)(arg0, &func_8021DCA0_5D9230);
    M2C_FIELD(arg0, u8 *, 0x74) = (u8) M2C_FIELD(&D_80162420_163020, u8 *, 0xD8);
    M2C_FIELD(&D_80162420_163020, u8 *, 0xD8) = (u8) (M2C_FIELD(&D_80162420_163020, u8 *, 0xD8) + 1);
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8021B3BC_5D694C)(arg0, 4, 0x3ECCCCCD, 1);
    ((M2C_UNK (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_08003464_73BFA4);

    *(volatile s32 *)0x80000000 = 1;
}
