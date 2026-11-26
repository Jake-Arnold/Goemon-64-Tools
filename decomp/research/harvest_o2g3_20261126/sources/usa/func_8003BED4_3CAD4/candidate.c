#include "m2c_types.h"
extern void *D_801C1728_1C2328;
extern u8 *D_801C172C_1C232C;

void func_8003BED4_3CAD4(void) {
    M2C_FIELD(D_801C1728_1C2328, s16 *, 0x2E) = (s16) (*D_801C172C_1C232C << 8);
    D_801C172C_1C232C += 1;
}
