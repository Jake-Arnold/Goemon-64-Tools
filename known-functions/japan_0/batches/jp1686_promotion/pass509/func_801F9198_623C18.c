#include "m2c_types.h"
s32 func_8000DB18_E718(M2C_UNK);                    /* extern */
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
f32 func_801D8660_6030E0(M2C_UNK, M2C_UNK);         /* extern */
M2C_UNK func_801FD820_6282A0(s32, s32);             /* extern */
M2C_UNK func_801F8D64_6237E4();                     /* static */

void func_801F9198_623C18(s32 arg0, M2C_UNK arg1) {
    if (func_801D8660_6030E0(arg1, 0x41F00000) == 0.0f) {
        func_801FD820_6282A0(arg0, func_8000DB18_E718(5) & 0xFF);
        func_80034E8C_35A8C(func_801F8D64_6237E4);
    }
}
