#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D8604_603084(s32, M2C_UNK *);       /* extern */
f32 func_801D8660_6030E0(s32, M2C_UNK);             /* extern */
M2C_UNK func_801DB75C_6061DC(void *);               /* extern */
M2C_UNK func_801F92DC_623D5C();                     /* static */
M2C_UNK func_801FCE00_627880();                     /* static */
extern M2C_UNK D_80210990_63B410;

void func_801F9250_623CD0(void *arg0, s32 arg1) {
    func_801FCE00_627880();
    func_801DB75C_6061DC(arg0);
    if (func_801D8660_6030E0(arg1, 0x42480000) == 0.0f) {
        func_801D8604_603084(arg1, &D_80210990_63B410);
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x28;
        M2C_FIELD(arg0, s32 *, 0x84) = 0;
        M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x74) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
        func_80034E8C_35A8C(func_801F92DC_623D5C);
    }
}
