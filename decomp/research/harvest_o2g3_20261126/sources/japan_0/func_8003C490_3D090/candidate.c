#include "m2c_types.h"
extern void *D_80178E00_179A00;
extern u8 *D_80178E04_179A04;

void func_8003C490_3D090(void) {
    M2C_FIELD(D_80178E00_179A00, s8 *, 0x8C) = 1;
    M2C_FIELD(D_80178E00_179A00, s16 *, 0x8A) = (s16) *D_80178E04_179A04;
    D_80178E04_179A04 += 1;
}
