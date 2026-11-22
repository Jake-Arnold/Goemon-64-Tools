#include "m2c_types.h"
f32 func_801D8660_6030E0(s32, M2C_UNK);             /* extern */
M2C_UNK func_801DB804_606284(s32);                  /* extern */
M2C_UNK func_801F5C70_6206F0(s32);                  /* static */
s32 func_801FCA5C_6274DC(s32);                      /* static */
M2C_UNK func_801FCE00_627880();                     /* static */

void func_801F9C6C_6246EC(s32 arg0, s32 arg1) {
    func_801FCE00_627880();
    func_801DB804_606284(arg0);
    if ((func_801FCA5C_6274DC(arg0) != 0) && (func_801D8660_6030E0(arg1, 0xC2480000) == 0.0f)) {
        func_801F5C70_6206F0(arg0);
    }
}
