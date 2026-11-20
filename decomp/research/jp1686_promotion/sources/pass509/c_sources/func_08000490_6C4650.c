#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021BB8C_5D711C;
M2C_UNK func_080003B0_6C4570();                     /* static */

void func_08000490_6C4650(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x33C;
    M2C_FIELD(arg0, s32 *, 0x60) = 0x80000020;
    if (M2C_FIELD(arg0, s32 *, 0xD0) == 1) {
        M2C_FIELD(arg0, s32 *, 0x60) = 0x80000000;
    }
    ((M2C_UNK(*)())&func_8021BB8C_5D711C)(arg0, 0);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080003B0_6C4570);
}
