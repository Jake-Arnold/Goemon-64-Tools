#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_8020D338_637DB8();                     /* static */
extern f64 D_802145D0_63F050;
extern s8 *D_80214600_63F080;

void func_8020D284_637D04(s32 arg0, M2C_UNK arg1) {
    f32 temp_f0;
    s8 *temp_v0;

    temp_v0 = D_80214600_63F080 + 0xA0;
    temp_f0 = M2C_FIELD(temp_v0, f32 *, 8);
    if (temp_f0 < -500.0f) {
        M2C_FIELD(temp_v0, f32 *, 8) = (f32) ((f64) temp_f0 + 0.5);
    } else {
        M2C_FIELD(D_80214600_63F080, s8 *, 0x2C1) = 1;
        M2C_FIELD(temp_v0, f32 *, 8) = (f32) ((f64) M2C_FIELD(temp_v0, f32 *, 8) + D_802145D0_63F050);
    }
    if (M2C_FIELD(temp_v0, f32 *, 8) > -300.0f) {
        M2C_FIELD(temp_v0, f32 *, 8) = -300.0f;
        func_80034E8C_35A8C(func_8020D338_637DB8);
    }
}
