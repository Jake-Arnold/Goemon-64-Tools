#include "m2c_types.h"
extern void *D_80178E00_179A00;
extern u8 *D_80178E04_179A04;

void func_8003B080_3BC80(void) {
    M2C_FIELD(D_80178E00_179A00, s16 *, 0x18) = (s16) (*D_80178E04_179A04 << 8);
    D_80178E04_179A04 += 1;
    M2C_FIELD(D_80178E00_179A00, s8 *, 0x1D) = 0;
}
