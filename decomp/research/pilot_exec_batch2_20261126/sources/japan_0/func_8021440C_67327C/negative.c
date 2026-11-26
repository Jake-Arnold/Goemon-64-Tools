#include "m2c_types.h"
extern u8 D_8021BBBC_67AA2C[][0x16];

u8 func_8021440C_67327C(s32 arg0) {
    if (arg0 >= 0xF) {
        { *(volatile int *)0x80000000 = 1; } return 0U;
    }
    return D_8021BBBC_67AA2C[arg0][0];
}
