#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80200150_5BC120;
extern char func_80224F80_5E0510;
M2C_UNK func_08004CB4_6FC844();                     /* static */
extern M2C_UNK g_system;

void func_08004C58_6FC7E8(M2C_UNK arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80224F80_5E0510)(arg0, 0x14) == 0) {
        ((M2C_UNK(*)())&func_80200150_5BC120)();
        M2C_FIELD(&g_system, s8 *, 0xCF8A2) = 0;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08004CB4_6FC844);
    }
}
