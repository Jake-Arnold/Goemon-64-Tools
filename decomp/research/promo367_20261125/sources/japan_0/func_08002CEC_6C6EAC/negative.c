#include "m2c_types.h"
extern char func_80023AB0_246B0;
extern char func_80023B00_24700;
extern char func_80034E8C_35A8C;
extern f64 D_08008A08_6CCBC8;
extern M2C_UNK func_08002D64_6C6F24;

void func_08002CEC_6C6EAC(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v0;

    M2C_FIELD(arg1, f32 *, 0xC) = (f32) ((f64) M2C_FIELD(arg1, f32 *, 0xC) + D_08008A08_6CCBC8);
    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        ((M2C_UNK(*)())&func_80023B00_24700)(1);
        ((M2C_UNK(*)())&func_80023AB0_246B0)(3);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08002D64_6C6F24);
    }
}
