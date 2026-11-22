#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_801FF330_5BB300;
extern char func_80224F80_5E0510;
M2C_UNK func_08004F68_6FCAF8();                     /* static */
extern M2C_UNK g_system;

void func_08004EEC_6FCA7C(M2C_UNK arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80224F80_5E0510)(arg0, 0x14) == 0) {
        ((M2C_UNK(*)())&func_801FF330_5BB300)(0x139, 0x50, 0x50, 0xFA, 0, 0x50, 0x200);
        M2C_FIELD(&g_system, s8 *, 0xCF8A2) = 0;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08004F68_6FCAF8);
    }
}
