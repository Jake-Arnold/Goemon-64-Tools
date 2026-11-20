#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern char func_8021E548_5D9AD8;
M2C_UNK func_0800212C_6B9EAC();                     /* static */

void func_080020C4_6B9E44(s32 arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_8021E548_5D9AD8)(arg0, 8) == 0) {
        ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 1, 0x3E2AAAAB, 0);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_0800212C_6B9EAC);
    }
}
