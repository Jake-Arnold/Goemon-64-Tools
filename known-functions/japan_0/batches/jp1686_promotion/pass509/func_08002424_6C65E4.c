#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80224ED8_5E0468;
M2C_UNK func_08002470_6C6630();                     /* static */
extern M2C_UNK g_system;

void func_08002424_6C65E4(M2C_UNK arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80224ED8_5E0468)(arg0, 0x32) == 0) {
        M2C_FIELD(&g_system, s8 *, 0xCF8A2) = 0;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08002470_6C6630);
    }
}
