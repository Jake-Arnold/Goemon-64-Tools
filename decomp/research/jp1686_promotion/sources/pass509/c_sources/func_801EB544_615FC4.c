#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
f32 func_801D8660_6030E0(void *, M2C_UNK, void *, void *); /* extern */
M2C_UNK func_801EB610_616090();                     /* static */

void func_801EB544_615FC4(void *arg0, void *arg1) {
    if (func_801D8660_6030E0(arg1, 0x41200000, arg0, arg1) == 0.0f) {
        if (M2C_FIELD(arg1, f32 *, 0x10) >= -350.0f) {
            M2C_FIELD(arg0, f32 *, 0x78) = -10.0f;
        } else {
            M2C_FIELD(arg0, f32 *, 0x78) = -4.0f;
        }
        if (M2C_FIELD(arg1, f32 *, 8) >= 0.0f) {
            M2C_FIELD(arg0, f32 *, 0x70) = -8.0f;
        } else {
            M2C_FIELD(arg0, f32 *, 0x70) = 8.0f;
        }
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x1E;
        func_80034E8C_35A8C(func_801EB610_616090);
    }
}
