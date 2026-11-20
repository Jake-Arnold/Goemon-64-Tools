#include "m2c_types.h"
M2C_UNK func_80034B44_35744();                      /* extern */
M2C_UNK func_801DB78C_60620C();                     /* extern */
M2C_UNK func_801DC234_606CB4(void *, M2C_UNK);      /* extern */
M2C_UNK func_801DC270_606CF0(void *, M2C_UNK);      /* extern */
extern f64 D_802145C0_63F040;
extern void *D_80214600_63F080;

void func_8020D010_637A90(void *arg0, void *arg1) {
    f64 temp_f0;

    temp_f0 = (f64) M2C_FIELD(arg0, f32 *, 0x78);
    if (temp_f0 >= 14.0) {
        M2C_FIELD(arg0, f32 *, 0x78) = 14.0f;
    } else {
        M2C_FIELD(arg0, f32 *, 0x78) = (f32) (temp_f0 + D_802145C0_63F040);
    }
    func_801DB78C_60620C();
    func_801DC234_606CB4(arg0, 0x3DCCCCCD);
    func_801DC270_606CF0(arg0, 0x3DCCCCCD);
    if (M2C_FIELD(arg1, f32 *, 0x10) >= -100.0f) {
        func_80034B44_35744();
        return;
    }
    if (M2C_FIELD(D_80214600_63F080, u8 *, 0x2C4) == 1) {
        func_80034B44_35744();
    }
}
