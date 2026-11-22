#include "m2c_types.h"
M2C_UNK func_80034E9C_35A9C(s32, M2C_UNK (*)());    /* extern */
M2C_UNK func_80205DEC_63086C();                     /* static */
extern void *D_80214600_63F080;
extern void *func_80214670_5CFC00;

void func_80205AA8_630528(s32 arg0, M2C_UNK arg1) {
    u8 temp_v0;

    temp_v0 = M2C_FIELD(func_80214670_5CFC00, u8 *, 4);
    if ((temp_v0 != 0) && (temp_v0 == 1)) {
        func_80034E9C_35A9C(M2C_FIELD(D_80214600_63F080, s32 *, 0x1D8), func_80205DEC_63086C);
        M2C_FIELD(func_80214670_5CFC00, u8 *, 4) = (u8) (M2C_FIELD(func_80214670_5CFC00, u8 *, 4) | 0x50);
    }
}
