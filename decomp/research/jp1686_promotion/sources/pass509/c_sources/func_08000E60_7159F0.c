#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern char func_8022B618_5E6BA8;
M2C_UNK func_08000EC4_715A54();                     /* static */

void func_08000E60_7159F0(s32 arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_8022B618_5E6BA8)() == 1) {
        ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 0, 0x3E800000, 1);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000EC4_715A54);
    }
}
