#include "m2c_types.h"
M2C_UNK func_8000DB18_E718(M2C_UNK);                /* extern */
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D156C_5FBFEC();                     /* static */
extern void *D_80214600_63F080;

void func_801D1740_5FC1C0(s32 arg0, M2C_UNK arg1) {
    if (M2C_FIELD(D_80214600_63F080, u8 *, 0x2C4) == 0) {
        func_80034E8C_35A8C(func_801D156C_5FBFEC);
    }
    func_8000DB18_E718(0x11B7);
    M2C_FIELD(D_80214600_63F080, s32 *, 0x2C8) = (s32) (M2C_FIELD(D_80214600_63F080, s32 *, 0x2C8) + 1);
}
