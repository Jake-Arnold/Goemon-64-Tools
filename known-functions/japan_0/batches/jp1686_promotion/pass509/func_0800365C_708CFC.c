#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80224ED8_5E0468;
M2C_UNK func_080036B0_708D50();                     /* static */

void func_0800365C_708CFC(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80224ED8_5E0468)(arg0, 0x50) == 0) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 5;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080036B0_708D50);
    }
}
