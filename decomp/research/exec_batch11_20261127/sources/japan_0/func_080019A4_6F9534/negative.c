#include "m2c_types.h"

extern u8 func_80034E8C_35A8C[];
extern u8 func_08001B44_6F96D4[];

void func_080019A4_6F9534(void *arg0, s32 arg1) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0xDC);
    M2C_FIELD(temp_v0, u32 *, 0xEC) &= ~4;
    if (M2C_FIELD(arg0, u16 *, 0xDA) != 0) {
        M2C_FIELD(temp_v0, u32 *, 0xEC) |= 4;
        M2C_FIELD(arg0, u16 *, 0xDA) = 0;
    }
    if (M2C_FIELD(temp_v0, u32 *, 0xEC) & 1) {
        ((void (*)(void *))func_80034E8C_35A8C)(func_08001B44_6F96D4);
    }

    *(volatile int *)0x80000000 = 1;
}
