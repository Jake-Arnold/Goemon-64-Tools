#include "m2c_types.h"
extern char func_8003521C_35E1C;
M2C_UNK func_0800053C_6C874C();                     /* static */
extern f64 D_08006D98_6CEFA8;

void func_080004BC_6C86CC(void *arg0, void *arg1) {
    f32 temp_f0;

    temp_f0 = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0xD8) - D_08006D98_6CEFA8);
    M2C_FIELD(arg0, f32 *, 0xD8) = temp_f0;
    M2C_FIELD(arg1, f32 *, 0xC) = (f32) (M2C_FIELD(arg1, f32 *, 0xC) + temp_f0);
    if (M2C_FIELD(arg0, f32 *, 0xD8) <= 0.0f) {
        M2C_FIELD(arg0, s16 *, 0xD4) = 0x80;
        M2C_FIELD(arg1, u8 *, 0x7C) = (u8) (M2C_FIELD(arg1, u8 *, 0x7C) & 0xFFFD);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_0800053C_6C874C);
    }
}
