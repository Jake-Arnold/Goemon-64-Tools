#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_8021BB8C_5D711C(void *, M2C_UNK);      /* extern */
M2C_UNK func_8021DB18_5D90A8(void *, M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_8021EB78_5DA108(void *, M2C_UNK);      /* extern */
M2C_UNK func_80226800_5E1D90();                     /* extern */
M2C_UNK func_8021999C_5D4F2C();                     /* static */

void func_802199BC_5D4F4C(void *arg0, M2C_UNK arg1) {
    func_80226800_5E1D90();
    M2C_FIELD(arg0, s8 *, 0x6C) = 0;
    M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x80000000);
    func_8021BB8C_5D711C(arg0, 0);
    func_8021EB78_5DA108(arg0, 0x41200000);
    func_8021DB18_5D90A8(arg0, 0x64, 0xA, 0);
    M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & 0xF7FFFFFF);
    func_80034E8C_35A8C(func_8021999C_5D4F2C);
}
