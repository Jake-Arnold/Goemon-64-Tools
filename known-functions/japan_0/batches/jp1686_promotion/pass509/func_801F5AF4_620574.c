#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D8738_6031B8(s32, M2C_UNK);         /* extern */
M2C_UNK func_801F5B44_6205C4();                     /* static */
M2C_UNK func_801FC7A4_627224();                     /* static */
s32 func_801FCA5C_6274DC(void *);                   /* static */

void func_801F5AF4_620574(void *arg0, s32 arg1) {
    func_801FC7A4_627224();
    func_801D8738_6031B8(arg1, 0x42200000);
    if (func_801FCA5C_6274DC(arg0) != 0) {
        M2C_FIELD(arg0, s32 *, 0x7C) = 0;
        func_80034E8C_35A8C(func_801F5B44_6205C4);
    }
}
