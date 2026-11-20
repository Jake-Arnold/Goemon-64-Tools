#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_80038838_39438(M2C_UNK);               /* extern */
s32 func_801D8838_6032B8(s32, M2C_UNK, M2C_UNK);    /* extern */
f32 func_801D8910_603390(M2C_UNK, M2C_UNK);                  /* extern */
M2C_UNK func_801F4F48_61F9C8();                     /* static */

void func_801F4ED8_61F958(void *arg0, s32 arg1) {
    if (func_801D8910_603390(arg0, 0x42A00000) == 0.0f) {
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x1E;
        func_80034E8C_35A8C(func_801F4F48_61F9C8);
    }
    if (func_801D8838_6032B8(arg1, 0x42A00000, 0x40800000) != 0) {
        func_80038838_39438(0x153);
    }
}
