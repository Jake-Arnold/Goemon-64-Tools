#include "m2c_types.h"
extern char func_8021ADD0_5D62A0;
extern char func_8021B09C_5D656C;
extern char func_8021BB04_5D6FD4;
extern char func_8021BC04_5D70D4;

void func_08002714_6D8664(void *arg0, void *arg1) {
    f32 temp_f0;
    f32 temp_f2;

    ((M2C_UNK  (*)(void *, M2C_UNK, M2C_UNK))&func_8021BC04_5D70D4)(arg0, 0x3D4CCCCD, 0x41000000);
    ((M2C_UNK (*)(void *, f32, f32, M2C_UNK))&func_8021BB04_5D6FD4)(arg0, (f32) M2C_FIELD(arg0, s16 *, 0xA0), (f32) M2C_FIELD(arg0, s16 *, 0xA2), 0x40000000);
    M2C_FIELD(arg1, s16 *, 0x16) = ((s16 (*)(f32, f32))&func_8021ADD0_5D62A0)(M2C_FIELD(arg0, f32 *, 0x78), M2C_FIELD(arg0, f32 *, 0x80));
    temp_f0 = (f32) M2C_FIELD(arg0, s16 *, 0xA2) - M2C_FIELD(arg1, f32 *, 0x10);
    temp_f2 = (f32) M2C_FIELD(arg0, s16 *, 0xA0) - M2C_FIELD(arg1, f32 *, 8);
    if (((temp_f0 * temp_f0) + (temp_f2 * temp_f2)) < 900.0f) {
        M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
        ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK))&func_8021B09C_5D656C)(arg0, 0, 1);
    }

    *(volatile s32 *)0x80000000 = 1;
}
