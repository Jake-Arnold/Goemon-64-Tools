#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
M2C_UNK func_08000E2C_6C057C();                     /* static */
extern M2C_UNK D_8015CC30_15D830;

void func_08000DB4_6C0504(s32 arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    M2C_FIELD(&D_8015CC30_15D830, f32 *, 0x184) = (f32) M2C_FIELD(arg1, f32 *, 8);
    M2C_FIELD(&D_8015CC30_15D830, f32 *, 0x188) = (f32) M2C_FIELD(arg1, f32 *, 0xC);
    M2C_FIELD(&D_8015CC30_15D830, f32 *, 0x18C) = (f32) M2C_FIELD(arg1, f32 *, 0x10);
    ((M2C_UNK(*)())&func_80038B98_39798)(0x154);
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08000E2C_6C057C, arg1);
    }
}
