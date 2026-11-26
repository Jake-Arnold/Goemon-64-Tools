#include "m2c_types.h"
extern void *D_80178E00_179A00;
extern u8 *D_80178E04_179A04;

void func_8003BB44_3C744(void) {
    M2C_FIELD(D_80178E00_179A00, s16 *, 0x2E) = (s16) (*D_80178E04_179A04 << 8);
    D_80178E04_179A04 += 1;

    *(volatile s32 *)0x80000000 = 1;
}
