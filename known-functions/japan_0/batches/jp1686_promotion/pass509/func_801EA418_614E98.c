#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_80037890_38490(M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_8003790C_3850C(M2C_UNK, M2C_UNK);      /* extern */
M2C_UNK func_80038838_39438(M2C_UNK);               /* extern */
f32 func_801D8660_6030E0(void *, M2C_UNK);          /* extern */
M2C_UNK func_801D88EC_60336C(void *, M2C_UNK *);    /* extern */
M2C_UNK func_801E608C_610B0C(M2C_UNK, s32, f32, s32); /* extern */
M2C_UNK func_801E67C0_611240(void *, s32, f32, s32); /* extern */
M2C_UNK func_801EA528_614FA8();                     /* static */
extern M2C_UNK D_80210900_63B380;
extern f64 D_80213640_63E0C0;

void func_801EA418_614E98(void *arg0, void *arg1) {
    if (func_801D8660_6030E0(arg1, 0xC3960000) == 0.0f) {
        func_801D88EC_60336C(arg0, &D_80210900_63B380);
        func_80038838_39438(0x4A);
        func_801E67C0_611240(arg0, M2C_FIELD(arg1, s32 *, 8), M2C_FIELD(arg1, f32 *, 0xC) + 50.0f, M2C_FIELD(arg1, s32 *, 0x10));
        func_801E608C_610B0C(1, M2C_FIELD(arg1, s32 *, 8), M2C_FIELD(arg1, f32 *, 0xC), M2C_FIELD(arg1, s32 *, 0x10));
        func_8003790C_3850C(0, 0x78);
        func_80037890_38490(0, 1, 0xAAAAAAAA);
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x78;
        M2C_FIELD(arg0, s32 *, 0x80) = 0;
        func_80034E8C_35A8C(func_801EA528_614FA8);
    }
    if (M2C_FIELD(arg1, f32 *, 0x28) > 13.0f) {
        M2C_FIELD(arg1, f32 *, 0xC) = (f32) ((f64) M2C_FIELD(arg1, f32 *, 0xC) + D_80213640_63E0C0);
    }
}
