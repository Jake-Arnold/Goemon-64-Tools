#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D8DDC_60385C(void *);               /* extern */
M2C_UNK func_801DE44C_608ECC();                     /* static */
M2C_UNK func_801DE528_608FA8(void *, s32);          /* static */
M2C_UNK func_801DE640_6090C0(void *, s32);          /* static */
M2C_UNK func_801DE750_6091D0(void *);               /* static */

void func_801DE3A4_608E24(void *arg0, M2C_UNK arg1) {
    s32 temp_a1;
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, s32 *, 0x98);
    M2C_FIELD(arg0, s32 *, 0x98) = (s32) (temp_v0 - 1);
    if (temp_v0 <= 0) {
        M2C_FIELD(arg0, s8 *, 0x30) = 0;
        func_80034E8C_35A8C(func_801DE44C_608ECC);
    }
    temp_a1 = M2C_FIELD(arg0, s32 *, 0x34);
    if (temp_a1 != 0) {
        if (M2C_FIELD(arg0, u8 *, 0x4C) == 0x3D) {
            func_801DE528_608FA8(arg0, temp_a1);
            M2C_FIELD(arg0, s8 *, 0x30) = 0;
            func_801D8DDC_60385C(arg0);
            M2C_FIELD(arg0, s32 *, 0x98) = 3;
        } else {
            func_801DE640_6090C0(arg0, temp_a1);
            M2C_FIELD(arg0, s8 *, 0x30) = 0;
            func_801D8DDC_60385C(arg0);
            M2C_FIELD(arg0, s32 *, 0x98) = 3;
        }
    }
    func_801DE750_6091D0(arg0);
}
