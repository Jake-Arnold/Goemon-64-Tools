#include "../m2c_types.h"
void func_08001A04_6B5904(void *arg0) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    M2C_FIELD(arg0, s32 *, 0x60) = 0x80000200;
    M2C_FIELD(arg0, s32 *, 0x64) = 2;
    M2C_FIELD(arg0, s32 *, 0xE0) = 0;
    M2C_FIELD(arg0, s16 *, 0xA4) = (s16) M2C_FIELD(arg0, s32 *, 0xD4);
    M2C_FIELD(temp_v0, f32 *, 0x1C) = 1.0f;
    M2C_FIELD(temp_v0, f32 *, 0x20) = 1.0f;
    M2C_FIELD(temp_v0, f32 *, 0x24) = 1.0f;
}
