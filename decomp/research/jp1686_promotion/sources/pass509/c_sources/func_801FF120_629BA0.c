#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801FF210_629C90();                     /* static */
extern f64 D_80213FD0_63EA50;
extern f64 D_80213FD8_63EA58;
extern s8 *D_80214600_63F080;

void func_801FF120_629BA0(s32 arg0, M2C_UNK arg1) {
    s32 var_a0;
    s8 *temp_v0;

    var_a0 = 0;
    temp_v0 = D_80214600_63F080 + 0xA0;
    if (M2C_FIELD(D_80214600_63F080, u8 *, 0x2C1) == 4) {
        M2C_FIELD(temp_v0, f32 *, 4) = (f32) ((f64) M2C_FIELD(temp_v0, f32 *, 4) + D_80213FD0_63EA50);
        if ((f64) M2C_FIELD(temp_v0, f32 *, 4) >= 0.0) {
            var_a0 = 1;
            M2C_FIELD(temp_v0, f32 *, 4) = 0.0f;
        }
        M2C_FIELD(temp_v0, f32 *, 0x10) = (f32) ((f64) M2C_FIELD(temp_v0, f32 *, 0x10) + D_80213FD8_63EA58);
        if ((f64) M2C_FIELD(temp_v0, f32 *, 0x10) >= 30.0) {
            var_a0 = (var_a0 + 1) & 0xFF;
            M2C_FIELD(temp_v0, f32 *, 0x10) = 30.0f;
        }
    }
    if (var_a0 == 2) {
        func_80034E8C_35A8C(func_801FF210_629C90);
    }
}
