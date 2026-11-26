#include "m2c_types.h"
extern void *D_801C1728_1C2328;
extern u8 *D_801C172C_1C232C;

void func_8003B410_3C010(void) {
    M2C_FIELD(D_801C1728_1C2328, s16 *, 0x18) = (s16) (*D_801C172C_1C232C << 8);
    D_801C172C_1C232C += 1;
    M2C_FIELD(D_801C1728_1C2328, s8 *, 0x1D) = 0;

    *(volatile s32 *)0x80000000 = 1;
}
