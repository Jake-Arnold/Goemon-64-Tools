#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801DB75C_6061DC();                     /* extern */
M2C_UNK func_801EC918_617398();                     /* static */
extern f64 D_80213808_63E288;

void func_801EC864_6172E4(void *arg0, void *arg1) {
    M2C_FIELD(arg0, f32 *, 0x74) = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0x74) + D_80213808_63E288);
    func_801DB75C_6061DC();
    if (M2C_FIELD(arg1, f32 *, 0xC) >= 400.0f) {
        M2C_FIELD(arg0, s32 *, 0xB0) = 0;
        M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x74) = 15.0f;
        if (M2C_FIELD(arg1, f32 *, 8) > 0.0f) {
            M2C_FIELD(arg0, s32 *, 0x98) = 0x190;
        } else {
            M2C_FIELD(arg0, s32 *, 0x98) = -0x190;
        }
        func_80034E8C_35A8C(func_801EC918_617398);
    }
}
