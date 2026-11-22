#include "m2c_types.h"
f32 func_80003D40_4940(u16);                        /* extern */
f32 func_80003DD0_49D0(u16);                        /* extern */
s32 func_8000DB18_E718(M2C_UNK);                    /* extern */
M2C_UNK func_80034E9C_35A9C(void *, M2C_UNK (*)()); /* extern */
M2C_UNK func_801D88EC_60336C(void *, M2C_UNK *);    /* extern */
M2C_UNK func_801F5F14_620994();                     /* static */
M2C_UNK func_801FC734_6271B4();                     /* static */
M2C_UNK func_801FC7A4_627224(void *);               /* static */
extern M2C_UNK D_802109A8_63B428;

void func_801F5DC0_620840(void *arg0, s32 arg1) {
    void *sp24;
    f32 temp_f2;

    func_801FC734_6271B4();
    func_801FC7A4_627224(arg0);
    sp24 = M2C_FIELD(arg0, void **, 0x18);
    func_801D88EC_60336C(arg0, &D_802109A8_63B428);
    M2C_FIELD(arg0, f32 *, 0x70) = (f32) ((f64) func_80003D40_4940(M2C_FIELD(sp24, u16 *, 0x16)) * 5.0);
    M2C_FIELD(arg0, f32 *, 0x78) = (f32) ((f64) func_80003DD0_49D0(M2C_FIELD(sp24, u16 *, 0x16)) * 5.0);
    temp_f2 = M2C_FIELD(sp24, f32 *, 8);
    if (temp_f2 >= 450.0f) {
        M2C_FIELD(arg0, f32 *, 0xB0) = -500.0f;
    } else if (temp_f2 <= -450.0f) {
        M2C_FIELD(arg0, f32 *, 0xB0) = 500.0f;
    } else if (func_8000DB18_E718(0x64) < 0x33) {
        M2C_FIELD(arg0, f32 *, 0xB0) = 500.0f;
    } else {
        M2C_FIELD(arg0, f32 *, 0xB0) = -500.0f;
    }
    M2C_FIELD(arg0, f32 *, 0xB8) = (f32) (func_8000DB18_E718(0xC8) - 0x258);
    M2C_FIELD(arg0, s32 *, 0x7C) = arg1;
    func_80034E9C_35A9C(arg0, func_801F5F14_620994);
}
