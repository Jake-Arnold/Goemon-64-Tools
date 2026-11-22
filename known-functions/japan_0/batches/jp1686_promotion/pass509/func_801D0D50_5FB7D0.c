#include "m2c_types.h"
M2C_UNK func_800134D0_140D0();                      /* extern */
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK osViSetSpecialFeatures(M2C_UNK);            /* extern */
M2C_UNK func_801D0D8C_5FB80C();                     /* static */

void func_801D0D50_5FB7D0(s32 arg0, M2C_UNK arg1) {
    osViSetSpecialFeatures(0x40);
    func_800134D0_140D0();
    func_80034E8C_35A8C(func_801D0D8C_5FB80C);
}
