#include "m2c_types.h"
M2C_UNK func_8003AFB0_3BBB0();                      /* extern */
extern void *D_801C1728_1C2328;

void func_8003B2B4_3BEB4(void) {
    M2C_FIELD(D_801C1728_1C2328, s8 *, 0x49) = 2;
    if (M2C_FIELD(D_801C1728_1C2328, u16 *, 0x52) != 0) {
        M2C_FIELD(D_801C1728_1C2328, s16 *, 0x4A) = 0;
        M2C_FIELD(D_801C1728_1C2328, u16 *, 0x4C) = (u16) M2C_FIELD(D_801C1728_1C2328, u16 *, 0x52);
        func_8003AFB0_3BBB0();
    }
}
