#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_80218D7C_5D424C;
extern char func_80218DA8_5D4278;
extern char func_8021927C_5D474C;
extern char func_8021A644_5D5B14;
M2C_UNK func_080015D4_6E0774();                     /* static */

void func_08001508_6E06A8(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_8021A644_5D5B14)();
    M2C_FIELD(arg0, s32 *, 0x60) = 0x2E86E0;
    M2C_FIELD(arg0, s8 *, 0x8E) = 5;
    M2C_FIELD(arg0, s8 *, 0x8F) = 6;
    ((M2C_UNK(*)())&func_8021927C_5D474C)(arg0);
    ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 0, 0x3EAAAAAB, 0);
    ((M2C_UNK(*)())&func_80218D7C_5D424C)(arg0, 0x3C, 0x96, 0);
    ((M2C_UNK(*)())&func_80218DA8_5D4278)(arg0, 0x3C, 0x3C, 0);
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080015D4_6E0774);
}
