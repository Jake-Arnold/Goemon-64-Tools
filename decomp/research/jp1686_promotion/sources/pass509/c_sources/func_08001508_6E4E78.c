#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern char func_8021DAEC_5D907C;
extern char func_8021DB18_5D90A8;
extern char func_8021DFEC_5D957C;
extern char func_8021F3B4_5DA944;
M2C_UNK func_080015D4_6E4F44();                     /* static */

void func_08001508_6E4E78(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_8021F3B4_5DA944)();
    M2C_FIELD(arg0, s32 *, 0x60) = 0x2E86E0;
    M2C_FIELD(arg0, s8 *, 0x8E) = 5;
    M2C_FIELD(arg0, s8 *, 0x8F) = 6;
    ((M2C_UNK(*)())&func_8021DFEC_5D957C)(arg0);
    ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 0, 0x3EAAAAAB, 0);
    ((M2C_UNK(*)())&func_8021DAEC_5D907C)(arg0, 0x3C, 0x96, 0);
    ((M2C_UNK(*)())&func_8021DB18_5D90A8)(arg0, 0x3C, 0x3C, 0);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080015D4_6E4F44);
}
