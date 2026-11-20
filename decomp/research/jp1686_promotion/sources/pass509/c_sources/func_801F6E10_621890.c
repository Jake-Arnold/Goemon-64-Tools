#include "m2c_types.h"
f32 func_801D8660_6030E0(s32, M2C_UNK);             /* extern */
M2C_UNK func_801DB75C_6061DC(s32);                  /* extern */
M2C_UNK func_801F5C70_6206F0(s32);                  /* static */
M2C_UNK func_801FCE00_627880();                     /* static */

void func_801F6E10_621890(s32 arg0, s32 arg1) {
    func_801FCE00_627880();
    func_801DB75C_6061DC(arg0);
    if (func_801D8660_6030E0(arg1, 0x42480000) == 0.0f) {
        func_801F5C70_6206F0(arg0);
    }
}
