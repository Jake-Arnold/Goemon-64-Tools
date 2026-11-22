#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D8910_603390(M2C_UNK, M2C_UNK);              /* extern */
u8 func_801D9238_603CB8(void *, M2C_UNK, M2C_UNK);  /* extern */
s32 func_801D9620_6040A0(void *, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801DB804_606284(void *);               /* extern */
M2C_UNK func_801EA874_6152F4();                     /* static */
M2C_UNK func_801F45F0_61F070(void *);               /* static */
extern f64 D_80213648_63E0C8;
extern f64 D_80213650_63E0D0;

void func_801EA794_615214(void *arg0, void *arg1) {
    u8 sp27;
    f64 temp_f0;

    func_801D8910_603390(arg0, 0x42700000);
    sp27 = func_801D9238_603CB8(arg0, 0x42A00000, 0xA);
    sp27 += func_801D9620_6040A0(arg0, 0, 0xA);
    func_801DB804_606284(arg0);
    func_801F45F0_61F070(arg0);
    temp_f0 = (f64) M2C_FIELD(arg1, f32 *, 0x10);
    if ((temp_f0 < D_80213648_63E0C8) && (D_80213650_63E0D0 < temp_f0)) {
        M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x74) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
        if (sp27 == 2) {
            M2C_FIELD(arg0, s32 *, 0x7C) = 0x64;
            func_80034E8C_35A8C(func_801EA874_6152F4);
        }
    }
}
