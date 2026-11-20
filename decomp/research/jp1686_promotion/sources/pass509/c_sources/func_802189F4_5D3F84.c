#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)(), void *); /* extern */
M2C_UNK func_80218A44_5D3FD4();                     /* static */

void func_802189F4_5D3F84(void *arg0, M2C_UNK arg1) {
    u16 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    if (temp_v0 != 0) {
        M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
        return;
    }
    M2C_FIELD(arg0, s32 *, 0x64) = (s32) (M2C_FIELD(arg0, s32 *, 0x64) | 2);
    func_80034E8C_35A8C(func_80218A44_5D3FD4, arg0);
}
