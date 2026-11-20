#include "../m2c_types.h"
void func_801EA30C_5A62DC(void *arg0) {
    M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x6C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x68) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0xE8) = 0.0f;
    *M2C_FIELD(arg0, s16 **, 0x5C) = 1;
    M2C_FIELD(arg0, u8 *, 0x30) = (u8) (M2C_FIELD(arg0, u8 *, 0x30) & 0xFFFE);
}
