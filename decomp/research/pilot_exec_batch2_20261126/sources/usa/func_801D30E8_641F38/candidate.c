#include "m2c_types.h"
void func_801D30E8_641F38(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, s32 *, 0xA0);
    M2C_FIELD(arg0, f32 *, 0x64) = M2C_FIELD(arg0, f32 *, 0x64) + ((f32) temp_v0 / 1000.0f);
    temp_v0 += M2C_FIELD(arg0, s32 *, 0xA4);
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, s8 *, 0x9C) = 0;
    }
    M2C_FIELD(arg0, s32 *, 0xA0) = temp_v0;
}
