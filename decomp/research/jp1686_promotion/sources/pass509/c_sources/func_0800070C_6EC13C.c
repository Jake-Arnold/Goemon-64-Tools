#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern char func_8021DB18_5D90A8;
extern char func_8021EBE0_5DA170;
extern char func_8021F3B4_5DA944;
extern char func_8022982C_5E4DBC;
extern char func_8022B5B0_5E6B40;
M2C_UNK func_080007E0_6EC210();                     /* static */

void func_0800070C_6EC13C(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_8021F3B4_5DA944)();
    M2C_FIELD(arg0, s32 *, 0x60) = 0x2006E3;
    ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 0, 0x3E800000, 1);
    ((M2C_UNK(*)())&func_8022982C_5E4DBC)(arg0, 0, 0x3F800000, 1);
    ((M2C_UNK(*)())&func_8021DB18_5D90A8)(arg0, 0x28, 0x28, 0);
    ((M2C_UNK(*)())&func_8021EBE0_5DA170)(arg0, 5, 0);
    ((M2C_UNK(*)())&func_8022B5B0_5E6B40)(arg0, M2C_FIELD(arg0, u16 *, 0xD2));
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080007E0_6EC210);
}
