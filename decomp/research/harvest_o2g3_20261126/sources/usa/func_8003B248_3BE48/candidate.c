#include "m2c_types.h"
M2C_UNK func_8003AFB0_3BBB0();                      /* extern */
M2C_UNK func_8003B2B4_3BEB4();                      /* extern */
extern void *D_801C1728_1C2328;

void func_8003B248_3BE48(void) {
    if (M2C_FIELD(D_801C1728_1C2328, u16 *, 0x54) != 0) {
        M2C_FIELD(D_801C1728_1C2328, s8 *, 0x49) = 1;
        M2C_FIELD(D_801C1728_1C2328, u16 *, 0x4A) = (u16) (M2C_FIELD(D_801C1728_1C2328, u16 *, 0x4A) - M2C_FIELD(D_801C1728_1C2328, u16 *, 0x54));
        M2C_FIELD(D_801C1728_1C2328, u16 *, 0x4C) = (u16) M2C_FIELD(D_801C1728_1C2328, u16 *, 0x50);
        func_8003AFB0_3BBB0();
        return;
    }
    func_8003B2B4_3BEB4();
}
