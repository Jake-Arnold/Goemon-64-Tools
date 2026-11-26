#include "m2c_types.h"
extern void *D_80178E00_179A00;
extern s8 *D_80178E04_179A04;

void func_8003BB78_3C778(void) {
    M2C_FIELD(D_80178E00_179A00, s16 *, 0x30) = (s16) (*D_80178E04_179A04 * 4);
    D_80178E04_179A04 += 1;
}
