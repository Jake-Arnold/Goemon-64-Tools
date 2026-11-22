#include "m2c_types.h"
M2C_UNK func_8000F198_FD98(M2C_UNK, s32, void *, M2C_UNK); /* extern */
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D8660_6030E0(void *, M2C_UNK);      /* extern */
M2C_UNK func_801DB844_6062C4(void *);               /* extern */
M2C_UNK func_801DBC28_6066A8(void *, M2C_UNK);              /* extern */
M2C_UNK func_801F6948_6213C8();                     /* static */
s32 func_801FC8BC_62733C(void *, f32);              /* static */
M2C_UNK func_801FCC14_627694(void *, M2C_UNK, M2C_UNK, M2C_UNK); /* static */
extern s32 D_80214600_63F080;

void func_801F6840_6212C0(void *arg0, void *arg1) {
    func_801DBC28_6066A8(arg0,0xBE4CCCCD);
    func_801DB844_6062C4(arg0);
    if (M2C_FIELD(arg0, f32 *, 0x74) < 1.0f) {
        func_801D8660_6030E0(arg1, 0x42700000);
        if ((f64) M2C_FIELD(arg1, f32 *, 0x28) >= 12.0) {
            M2C_FIELD(arg1, f32 *, 0x28) = 12.0f;
        }
        if (func_801FC8BC_62733C(arg0, M2C_FIELD(arg1, f32 *, 0x20) * 200.0f) == 0) {
            func_8000F198_FD98(0x282, D_80214600_63F080 + 0xA0, arg1, 0x44BB8000);
            func_801FCC14_627694(arg0, 0x3F333333, 0x3F000000, 0x3E99999A);
            func_80034E8C_35A8C(func_801F6948_6213C8);
        }
    }
}
