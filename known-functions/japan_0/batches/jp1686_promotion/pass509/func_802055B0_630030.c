#include "m2c_types.h"
s32 func_80014480_15080(s32, M2C_UNK);              /* extern */
s32 func_80034A78_35678(s32, M2C_UNK (*)(), M2C_UNK); /* extern */
s32 func_800372EC_37EEC();                          /* extern */
M2C_UNK func_80038838_39438(M2C_UNK);               /* extern */
M2C_UNK func_801D179C_5FC21C();                     /* extern */
M2C_UNK func_80205930_6303B0();                     /* extern */
M2C_UNK func_802051DC_62FC5C();                     /* static */
extern void *D_80214600_63F080;
extern s32 func_80214670_5CFC00;
extern s32 g_system_ptr;

s32 func_802055B0_630030(void) {
    s32 temp_v0;

    func_80214670_5CFC00 = 0;
    temp_v0 = func_80014480_15080(g_system_ptr + 0xC7FA4, 0x81C);
    if (temp_v0 == 0) {
        return 0;
    }
    func_80214670_5CFC00 = temp_v0;
    M2C_FIELD(D_80214600_63F080, s32 *, 0x1D0) = func_80034A78_35678(M2C_FIELD(D_80214600_63F080, s32 *, 0x1C4), func_802051DC_62FC5C, 0);
    M2C_FIELD(D_80214600_63F080, s32 *, 0x1D8) = func_80034A78_35678(M2C_FIELD(D_80214600_63F080, s32 *, 0x1C4), func_80205930_6303B0, 0);
    M2C_FIELD(D_80214600_63F080, s32 *, 0x1D4) = func_80034A78_35678(M2C_FIELD(D_80214600_63F080, s32 *, 0x1BC), func_801D179C_5FC21C, 0);
    if (func_800372EC_37EEC() == 0) {
        func_80038838_39438(0x35);
    } else {
        func_80038838_39438(0x36);
    }
    return M2C_FIELD(D_80214600_63F080, s32 *, 0x1D8);
}
