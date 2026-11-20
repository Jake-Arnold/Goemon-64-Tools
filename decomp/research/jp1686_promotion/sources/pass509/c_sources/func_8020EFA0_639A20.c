#include "m2c_types.h"
M2C_UNK func_80034B44_35744();                      /* extern */
M2C_UNK func_80038838_39438(M2C_UNK);               /* extern */
f32 func_801D8660_6030E0(void *, M2C_UNK, void *);  /* extern */
M2C_UNK func_801DB86C_6062EC(void *);               /* extern */
extern f64 D_802145E8_63F068;
extern f64 D_802145F0_63F070;

void func_8020EFA0_639A20(void *arg0, void *arg1) {
    if (func_801D8660_6030E0(arg1, 0x42700000, arg0) == 0.0f) {
        if (M2C_FIELD(arg0, s32 *, 0x90) == 0) {
            func_80038838_39438(0x14E);
            M2C_FIELD(arg0, s32 *, 0x90) = 1;
        }
        M2C_FIELD(arg0, f32 *, 0x74) = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0x74) + D_802145E8_63F068);
        if ((f64) M2C_FIELD(arg0, f32 *, 0x74) >= 2.0) {
            M2C_FIELD(arg0, f32 *, 0x74) = 2.0f;
        }
        M2C_FIELD(arg0, f32 *, 0x78) = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0x78) + D_802145F0_63F070);
        if ((f64) M2C_FIELD(arg0, f32 *, 0x78) >= 10.0) {
            M2C_FIELD(arg0, f32 *, 0x78) = 10.0f;
        }
        func_801DB86C_6062EC(arg0);
        if (M2C_FIELD(arg1, f32 *, 0x10) > 0.0f) {
            func_80034B44_35744();
        }
    }
}
