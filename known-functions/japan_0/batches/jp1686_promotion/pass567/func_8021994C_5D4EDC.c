#include "../m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_8021BB8C_5D711C(void *, M2C_UNK);      /* extern */
M2C_UNK func_80226800_5E1D90();                     /* extern */
M2C_UNK func_8021999C_5D4F2C();                     /* static */

void func_8021994C_5D4EDC(void *arg0, M2C_UNK arg1) {
    func_80226800_5E1D90();
    M2C_FIELD(arg0, s8 *, 0x6C) = 0;
    M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x80000000);
    func_8021BB8C_5D711C(arg0, 0);
    func_80034E8C_35A8C(func_8021999C_5D4F2C);
}
