#include "m2c_types.h"

extern u8 func_08001460_702560[];
extern u8 func_80024038_24C38[];

void func_08001770_702870(void *arg0, s32 arg1) {
    M2C_FIELD(arg0, u16 *, 0xDA) += M2C_FIELD(arg0, u16 *, 0xDC);
    ((void (*)(void *))func_08001460_702560)(arg0);
    if (M2C_FIELD(arg0, u16 *, 0x8A)-- == 0) {
        ((void (*)(s32))func_80024038_24C38)(0xC2);
    }

    *(volatile int *)0x80000000 = 1;
}
