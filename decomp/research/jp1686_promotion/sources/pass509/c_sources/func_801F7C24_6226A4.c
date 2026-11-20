#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D8738_6031B8(void *, M2C_UNK);      /* extern */
M2C_UNK func_801D88EC_60336C(void *, M2C_UNK *);    /* extern */
M2C_UNK func_801DB8BC_60633C(void *);               /* extern */
M2C_UNK func_801F7CD0_622750();                     /* static */
M2C_UNK func_801FCE00_627880(void *);               /* static */
extern M2C_UNK D_80210990_63B410;
extern f32 D_80213D84_63E804;
extern f32 D_80213D88_63E808;

void func_801F7C24_6226A4(void *arg0, void *arg1) {
    f32 temp_f0;

    func_801D8738_6031B8(arg1, 0x42200000);
    func_801FCE00_627880(arg0);
    func_801DB8BC_60633C(arg0);
    temp_f0 = M2C_FIELD(arg1, f32 *, 0x10);
    if ((temp_f0 <= D_80213D84_63E804) && (D_80213D88_63E808 <= temp_f0)) {
        M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x74) = 6.0f;
        func_801D88EC_60336C(arg0, &D_80210990_63B410);
        func_80034E8C_35A8C(func_801F7CD0_622750);
    }
}
