#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)(), void *); /* extern */
M2C_UNK func_802260A8_5E1638();                     /* static */
s32 func_802268EC_5E1E7C();                         /* static */

s32 func_80226060_5E15F0(void *arg0) {
    if (func_802268EC_5E1E7C() == 0) {
        return 0;
    }
    M2C_FIELD(arg0, s32 *, 0xB4) = (s32) M2C_FIELD(arg0, s32 *, 0xC);
    func_80034E8C_35A8C(func_802260A8_5E1638, arg0);
    return 1;
}
