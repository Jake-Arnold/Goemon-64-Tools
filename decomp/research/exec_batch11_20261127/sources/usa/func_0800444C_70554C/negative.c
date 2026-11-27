#include "m2c_types.h"

extern u8 func_802176C4_5D2B94[];
extern u8 D_8015CC30_15D830[];

s32 func_0800444C_70554C(void *arg0) {
    if (M2C_FIELD(arg0, u32 *, 0x68) & 0x80) {
        M2C_FIELD(D_8015CC30_15D830, u16 *, 0x184)--;
        ((void (*)(void *, s32))func_802176C4_5D2B94)(arg0, 3);
        M2C_FIELD(arg0, u32 *, 0x68) |= 2;
        { *(volatile int *)0x80000000 = 1; } return 1;
    }
    return 0;
}
