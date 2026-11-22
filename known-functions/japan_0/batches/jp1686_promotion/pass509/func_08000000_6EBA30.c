#include "m2c_types.h"
extern char func_8021B3BC_5D694C;
extern char func_8021DAEC_5D907C;
extern char func_8021DB18_5D90A8;
extern char func_8021DFEC_5D957C;
extern char func_8021EBE0_5DA170;
extern char func_8021F3B4_5DA944;
extern char func_8021FDD4_5DB364;
extern char func_8021FE0C_5DB39C;
extern char func_8022982C_5E4DBC;
M2C_UNK func_08000554_6EBF84();                     /* static */
extern M2C_UNK D_08001C80_6ED6B0;

void func_08000000_6EBA30(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_8021F3B4_5DA944)();
    M2C_FIELD(arg0, s32 *, 0x60) = 0x2006E3;
    ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 0, 0x3E800000, 1);
    ((M2C_UNK(*)())&func_8022982C_5E4DBC)(arg0, 0, 0x3F800000, 1);
    M2C_FIELD(arg0, s8 *, 0x8D) = 0x10;
    M2C_FIELD(arg0, M2C_UNK (**)(), 0x90) = func_08000554_6EBF84;
    ((M2C_UNK(*)())&func_8021DAEC_5D907C)(arg0, 0x32, 0x64, 0);
    ((M2C_UNK(*)())&func_8021DB18_5D90A8)(arg0, 0x190, 0x28, 0);
    ((M2C_UNK(*)())&func_8021DFEC_5D957C)(arg0);
    ((M2C_UNK(*)())&func_8021EBE0_5DA170)(arg0, 5, 0);
    ((M2C_UNK(*)())&func_8021FDD4_5DB364)(arg0, &D_08001C80_6ED6B0, 0);
    ((M2C_UNK(*)())&func_8021FE0C_5DB39C)(arg0, 0, 1);
}
