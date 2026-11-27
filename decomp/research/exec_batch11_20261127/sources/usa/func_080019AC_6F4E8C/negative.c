#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_08001B4C_6F502C[];

void func_080019AC_6F4E8C(void *arg0, s32 arg1) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0xDC);
    M2C_FIELD(temp_v0, u32 *, 0xEC) &= ~4;
    if (M2C_FIELD(arg0, u16 *, 0xDA) != 0) {
        M2C_FIELD(temp_v0, u32 *, 0xEC) |= 4;
        M2C_FIELD(arg0, u16 *, 0xDA) = 0;
    }
    if (M2C_FIELD(temp_v0, u32 *, 0xEC) & 1) {
        ((void (*)(void *))func_8003521C_35E1C)(func_08001B4C_6F502C);
    }

    *(volatile int *)0x80000000 = 1;
}
