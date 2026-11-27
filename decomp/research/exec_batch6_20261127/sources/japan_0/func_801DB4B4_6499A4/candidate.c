#include "m2c_types.h"
void func_801DB4B4_6499A4(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;
    s16 temp_v1;

    temp_v0 = M2C_FIELD(arg0, s32 *, 0xA8);
    M2C_FIELD(arg0, f32 *, 0x60) += (f32) temp_v0 / 1000.0f;
    temp_v1 = M2C_FIELD(arg0, s16 *, 0xA2) - 1;
    M2C_FIELD(arg0, s16 *, 0xA2) = temp_v1;
    if (temp_v1 == 0) {
        M2C_FIELD(arg0, s8 *, 0x9C) = 1;
        M2C_FIELD(arg0, s32 *, 0xAC) = -M2C_FIELD(arg0, s32 *, 0xAC);
    }
}
