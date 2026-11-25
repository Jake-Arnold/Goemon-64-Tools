#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80216E1C_5D22EC;
M2C_UNK func_080003B0_6BFB00();                     /* static */

void func_08000490_6BFBE0(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x33C;
    M2C_FIELD(arg0, s32 *, 0x60) = 0x80000020;
    if (M2C_FIELD(arg0, s32 *, 0xD0) == 1) {
        M2C_FIELD(arg0, s32 *, 0x60) = 0x80000000;
    }
    ((M2C_UNK(*)())&func_80216E1C_5D22EC)(arg0, 0);
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080003B0_6BFB00);
}
