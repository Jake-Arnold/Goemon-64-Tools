#include "m2c_types.h"
M2C_UNK func_80038838_39438(M2C_UNK);               /* extern */
f32 func_801D8910_603390(M2C_UNK, M2C_UNK);                  /* extern */
extern void *D_80214600_63F080;

void func_801EA268_614CE8(M2C_UNK arg0, void *arg1) {
    if (func_801D8910_603390(arg0, 0x42700000) == 0.0f) {
        if (M2C_FIELD(D_80214600_63F080, u8 *, 0x2C1) != 0) {
            func_80038838_39438(0x116);
            func_80038838_39438(0x11A);
            M2C_FIELD(arg1, s8 *, 5) = 7;
            M2C_FIELD(D_80214600_63F080, u8 *, 0x2C1) = 0U;
        }
    } else {
        M2C_FIELD(D_80214600_63F080, u8 *, 0x2C1) = 4U;
    }
}
