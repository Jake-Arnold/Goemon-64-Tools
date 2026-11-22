#include "m2c_types.h"
extern char func_80023AB0_246B0;
extern char func_80023CF8_248F8;
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
M2C_UNK func_080010B8_6C5278();                     /* static */
extern f32 D_080089BC_6CCB7C;
extern M2C_UNK D_80162420_163020;

void func_08001018_6C51D8(void *arg0, void *arg1) {
    M2C_FIELD(&D_80162420_163020, f32 *, 0x184) = (f32) M2C_FIELD(arg1, f32 *, 8);
    M2C_FIELD(&D_80162420_163020, f32 *, 0x188) = (f32) M2C_FIELD(arg1, f32 *, 0xC);
    M2C_FIELD(&D_80162420_163020, f32 *, 0x18C) = (f32) M2C_FIELD(arg1, f32 *, 0x10);
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((M2C_UNK(*)())&func_80023AB0_246B0)(7);
        ((M2C_UNK(*)())&func_80038808_39408)(0x154);
        ((M2C_UNK(*)())&func_80023CF8_248F8)(0x15E);
        M2C_FIELD(arg0, f32 *, 0x7C) = (f32) D_080089BC_6CCB7C;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080010B8_6C5278);
    }
}
