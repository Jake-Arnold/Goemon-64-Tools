#include "m2c_types.h"
extern void *D_80178E00_179A00;
extern u8 *D_80178E04_179A04;

void func_8003BF24_3CB24(void) {
    u8 temp_v0;

    temp_v0 = *D_80178E04_179A04;
    M2C_FIELD(D_80178E00_179A00, u8 *, 0x9E) = temp_v0;
    D_80178E04_179A04 += 1;
    if (temp_v0 != 0) {
        M2C_FIELD(D_80178E00_179A00, s16 *, 0xA0) = (s16) ((s32) M2C_FIELD(D_80178E00_179A00, u16 *, 0x9A) / (s32) M2C_FIELD(D_80178E00_179A00, u8 *, 0x9E));
    }

    *(volatile s32 *)0x80000000 = 1;
}
