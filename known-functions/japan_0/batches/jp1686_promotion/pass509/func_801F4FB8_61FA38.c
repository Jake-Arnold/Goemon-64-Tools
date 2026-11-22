#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D8910_603390(M2C_UNK, M2C_UNK);              /* extern */
M2C_UNK func_801F4FF8_61FA78();                     /* static */
s32 func_801FCA5C_6274DC(s32);                      /* static */

void func_801F4FB8_61FA38(s32 arg0, M2C_UNK arg1) {
    func_801D8910_603390(arg0, 0x42200000);
    if (func_801FCA5C_6274DC(arg0) != 0) {
        func_80034E8C_35A8C(func_801F4FF8_61FA78);
    }
}
