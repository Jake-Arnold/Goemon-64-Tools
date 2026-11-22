#include "m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_080004EC_6CD16C();                     /* static */
extern f64 D_08006D48_6D39C8;

void func_0800046C_6CD0EC(void *arg0, void *arg1) {
    f32 temp_f0;

    temp_f0 = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0xD8) - D_08006D48_6D39C8);
    M2C_FIELD(arg0, f32 *, 0xD8) = temp_f0;
    M2C_FIELD(arg1, f32 *, 0xC) = (f32) (M2C_FIELD(arg1, f32 *, 0xC) + temp_f0);
    if (M2C_FIELD(arg0, f32 *, 0xD8) <= 0.0f) {
        M2C_FIELD(arg0, s16 *, 0xD4) = 0x80;
        M2C_FIELD(arg1, u8 *, 0x7C) = (u8) (M2C_FIELD(arg1, u8 *, 0x7C) & 0xFFFD);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080004EC_6CD16C);
    }
}
