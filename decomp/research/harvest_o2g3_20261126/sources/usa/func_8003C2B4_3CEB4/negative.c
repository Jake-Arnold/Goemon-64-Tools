#include "m2c_types.h"
extern void *D_801C1728_1C2328;
extern u8 *D_801C172C_1C232C;

void func_8003C2B4_3CEB4(void) {
    u8 temp_v0;

    temp_v0 = *D_801C172C_1C232C;
    M2C_FIELD(D_801C1728_1C2328, u8 *, 0x9E) = temp_v0;
    D_801C172C_1C232C += 1;
    if (temp_v0 != 0) {
        M2C_FIELD(D_801C1728_1C2328, s16 *, 0xA0) = (s16) ((s32) M2C_FIELD(D_801C1728_1C2328, u16 *, 0x9A) / (s32) M2C_FIELD(D_801C1728_1C2328, u8 *, 0x9E));
    }

    *(volatile s32 *)0x80000000 = 1;
}
