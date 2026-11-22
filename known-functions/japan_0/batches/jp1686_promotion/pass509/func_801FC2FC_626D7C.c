#include "m2c_types.h"
f32 func_801D8660_6030E0(s32, M2C_UNK);             /* extern */
s32 func_801DC36C_606DEC(void *, M2C_UNK);          /* extern */
M2C_UNK func_801F5C70_6206F0(void *);               /* static */
M2C_UNK func_801FCA5C_6274DC();                     /* static */

void func_801FC2FC_626D7C(void *arg0, s32 arg1) {
    func_801FCA5C_6274DC();
    if ((func_801D8660_6030E0(arg1, 0xC1A00000) == 0.0f) && (func_801DC36C_606DEC(arg0, 0x3E4CCCCD) != 0)) {
        if (M2C_FIELD(arg0, s32 *, 0xEC) > 0) {
            M2C_FIELD(arg0, s32 *, 0xEC) = 0;
            M2C_FIELD(arg0, s32 *, 0xD4) = 0;
        }
        func_801F5C70_6206F0(arg0);
    }
}
