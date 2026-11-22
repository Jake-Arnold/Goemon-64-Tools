#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80224ED8_5E0468;
extern char func_80224FDC_5E056C;
M2C_UNK func_08004C58_6FC7E8();                     /* static */

void func_08004BF4_6FC784(s32 arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80224ED8_5E0468)(arg0, 0x50) == 0) {
        ((M2C_UNK(*)())&func_80224FDC_5E056C)(arg0, 0xFF, 0xFF, 0xFF);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08004C58_6FC7E8);
    }
}
