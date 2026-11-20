#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
M2C_UNK func_08000E2C_6C4FEC();                     /* static */
extern M2C_UNK D_80162420_163020;

void func_08000DB4_6C4F74(s32 arg0, void *arg1) {
    M2C_FIELD(&D_80162420_163020, f32 *, 0x184) = (f32) M2C_FIELD(arg1, f32 *, 8);
    M2C_FIELD(&D_80162420_163020, f32 *, 0x188) = (f32) M2C_FIELD(arg1, f32 *, 0xC);
    M2C_FIELD(&D_80162420_163020, f32 *, 0x18C) = (f32) M2C_FIELD(arg1, f32 *, 0x10);
    ((M2C_UNK(*)())&func_80038808_39408)(0x154);
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000E2C_6C4FEC, arg1);
    }
}
