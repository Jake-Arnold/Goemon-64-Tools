#include "m2c_types.h"
extern void *D_801C1728_1C2328;
extern s32 D_801C172C_1C232C;

void func_8003CB2C_3D72C(void) {
    M2C_FIELD(D_801C1728_1C2328, s32 *, 0x6C) = (s32) D_801C172C_1C232C;

    *(volatile s32 *)0x80000000 = 1;
}
