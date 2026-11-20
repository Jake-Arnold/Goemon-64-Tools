#include "m2c_types.h"
M2C_UNK func_8000F198_FD98(M2C_UNK, s32, void *, M2C_UNK); /* extern */
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801DB8BC_60633C();                     /* extern */
M2C_UNK func_801F81C8_622C48();                     /* static */
s32 func_801FC8BC_62733C(s32, f32);                 /* static */
M2C_UNK func_801FCC14_627694(s32, M2C_UNK, M2C_UNK, M2C_UNK); /* static */
extern s32 D_80214600_63F080;

void func_801F8134_622BB4(s32 arg0, void *arg1) {
    func_801DB8BC_60633C();
    if (func_801FC8BC_62733C(arg0, M2C_FIELD(arg1, f32 *, 0x20) * 350.0f) != 0) {
        func_8000F198_FD98(0x281, D_80214600_63F080 + 0xA0, arg1, 0x44BB8000);
        func_801FCC14_627694(arg0, 0x3F000000, 0x3ECCCCCD, 0x3E99999A);
        func_80034E8C_35A8C(func_801F81C8_622C48);
    }
}
