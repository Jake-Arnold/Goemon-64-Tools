#include "m2c_types.h"
extern char func_80023AB0_246B0;
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
extern char func_8021B3BC_5D694C;
M2C_UNK func_08000F34_6C50F4();                     /* static */
extern f32 D_080089B8_6CCB78;
extern M2C_UNK D_80162420_163020;

void func_08000E2C_6C4FEC(void *arg0, void *arg1) {
    f32 var_f0;

    M2C_FIELD(&D_80162420_163020, f32 *, 0x184) = (f32) M2C_FIELD(arg1, f32 *, 8);
    M2C_FIELD(&D_80162420_163020, f32 *, 0x188) = (f32) M2C_FIELD(arg1, f32 *, 0xC);
    M2C_FIELD(&D_80162420_163020, f32 *, 0x18C) = (f32) M2C_FIELD(arg1, f32 *, 0x10);
    M2C_FIELD(arg0, f32 *, 0x7C) = (f32) D_080089B8_6CCB78;
    var_f0 = M2C_FIELD(arg1, f32 *, 0xC);
    if (var_f0 < -20.0f) {
        ((M2C_UNK(*)())&func_80023AB0_246B0)(0xB);
        var_f0 = M2C_FIELD(arg1, f32 *, 0xC);
    }
    if (!(var_f0 > -60.0f)) {
        M2C_FIELD(arg1, f32 *, 0xC) = -60.0f;
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x01000000);
        ((M2C_UNK(*)())&func_80038808_39408)(0x155, arg1);
        ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 1, 0x3D088889, 0);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x3C;
        M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000F34_6C50F4);
    }
}
