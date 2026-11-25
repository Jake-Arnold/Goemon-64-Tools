#include "m2c_types.h"
extern char func_80023DF0_249F0;
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
extern char func_8021664C_5D1B1C;
M2C_UNK func_08000F34_6C0684();                     /* static */
extern f32 D_080089B8_6C8108;
extern M2C_UNK D_8015CC30_15D830;

void func_08000E2C_6C057C(void *arg0, void *arg1) {
    f32 var_f0;

    M2C_FIELD(&D_8015CC30_15D830, f32 *, 0x184) = (f32) M2C_FIELD(arg1, f32 *, 8);
    M2C_FIELD(&D_8015CC30_15D830, f32 *, 0x188) = (f32) M2C_FIELD(arg1, f32 *, 0xC);
    M2C_FIELD(&D_8015CC30_15D830, f32 *, 0x18C) = (f32) M2C_FIELD(arg1, f32 *, 0x10);
    M2C_FIELD(arg0, f32 *, 0x7C) = (f32) D_080089B8_6C8108;
    var_f0 = M2C_FIELD(arg1, f32 *, 0xC);
    if (var_f0 < -20.0f) {
        ((M2C_UNK(*)())&func_80023DF0_249F0)(0xB);
        var_f0 = M2C_FIELD(arg1, f32 *, 0xC);
    }
    if (!(var_f0 > -60.0f)) {
        M2C_FIELD(arg1, f32 *, 0xC) = -60.0f;
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x01000000);
        ((M2C_UNK(*)())&func_80038B98_39798)(0x155, arg1);
        ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 1, 0x3D088889, 0);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x3C;
        M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08000F34_6C0684);
    }
}
