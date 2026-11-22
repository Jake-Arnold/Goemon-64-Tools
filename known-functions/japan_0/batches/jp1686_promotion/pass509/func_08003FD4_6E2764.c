#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021E548_5D9AD8;
M2C_UNK func_08004024_6E27B4();                     /* static */

void func_08003FD4_6E2764(M2C_UNK arg0, void *arg1) {
    if (((s32(*)())&func_8021E548_5D9AD8)(arg0, 0x10) == 0) {
        M2C_FIELD(arg1, s8 *, 0x7C) = 4;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08004024_6E27B4);
    }
}
