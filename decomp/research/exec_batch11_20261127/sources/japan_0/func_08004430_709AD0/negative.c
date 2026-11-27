#include "m2c_types.h"

extern u8 func_8021C434_5D79C4[];
extern u8 D_80162420_163020[];

s32 func_08004430_709AD0(void *arg0) {
    if (M2C_FIELD(arg0, u32 *, 0x68) & 0x80) {
        M2C_FIELD(D_80162420_163020, u16 *, 0x184)--;
        ((void (*)(void *, s32))func_8021C434_5D79C4)(arg0, 3);
        M2C_FIELD(arg0, u32 *, 0x68) |= 2;
        { *(volatile int *)0x80000000 = 1; } return 1;
    }
    return 0;
}
