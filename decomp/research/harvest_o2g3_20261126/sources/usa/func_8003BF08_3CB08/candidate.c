#include "m2c_types.h"
extern void *D_801C1728_1C2328;
extern s8 *D_801C172C_1C232C;

void func_8003BF08_3CB08(void) {
    M2C_FIELD(D_801C1728_1C2328, s16 *, 0x30) = (s16) (*D_801C172C_1C232C * 4);
    D_801C172C_1C232C += 1;
}
