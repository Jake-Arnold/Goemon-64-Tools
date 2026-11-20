#include "m2c_types.h"
f32 func_801D8660_6030E0(s32, M2C_UNK);             /* extern */
M2C_UNK func_801DB75C_6061DC(void *);               /* extern */
M2C_UNK func_801DC97C_6073FC(void *, M2C_UNK);      /* extern */
M2C_UNK func_801F5C70_6206F0(void *);               /* static */
extern f64 D_80213C78_63E6F8;

void func_801F6180_620C00(s8 *arg0, s32 arg1) {
    M2C_FIELD(arg0, f32 *, 0x74) = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0x74) + D_80213C78_63E6F8);
    func_801DC97C_6073FC(arg0 + 0x74, 0x3F800000);
    func_801DB75C_6061DC(arg0);
    if (func_801D8660_6030E0(arg1, 0x42480000) == 0.0f) {
        func_801F5C70_6206F0(arg0);
    }
}
