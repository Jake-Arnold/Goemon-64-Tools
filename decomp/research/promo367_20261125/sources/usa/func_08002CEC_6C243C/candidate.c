#include "m2c_types.h"
extern char func_80023DF0_249F0;
extern char func_80023E40_24A40;
extern char func_8003521C_35E1C;
extern f64 D_08008A08_6C8158;
extern M2C_UNK func_08002D64_6C24B4;

void func_08002CEC_6C243C(void *arg0, void *arg1) {
    s32 temp_v0;

    M2C_FIELD(arg1, f32 *, 0xC) = (f32) ((f64) M2C_FIELD(arg1, f32 *, 0xC) + D_08008A08_6C8158);
    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        ((M2C_UNK(*)())&func_80023E40_24A40)(1);
        ((M2C_UNK(*)())&func_80023DF0_249F0)(3);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08002D64_6C24B4);
    }
}
