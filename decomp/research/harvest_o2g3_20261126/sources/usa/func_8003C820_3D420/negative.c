#include "m2c_types.h"
extern void *D_801C1728_1C2328;
extern u8 *D_801C172C_1C232C;

void func_8003C820_3D420(void) {
    M2C_FIELD(D_801C1728_1C2328, s8 *, 0x8C) = 1;
    M2C_FIELD(D_801C1728_1C2328, s16 *, 0x8A) = (s16) *D_801C172C_1C232C;
    D_801C172C_1C232C += 1;

    *(volatile s32 *)0x80000000 = 1;
}
