#include "../m2c_types.h"
void func_801E50C8_6535B8(void *arg0, void *arg1) {
    void *temp_v0;
    void *temp_v1;

    temp_v0 = M2C_FIELD(arg0, void **, 0x6C);
    M2C_FIELD(arg0, f32 *, 0x7C) = (f32) M2C_FIELD(temp_v0, f32 *, 0x5C);
    M2C_FIELD(arg0, f32 *, 0x80) = (f32) M2C_FIELD(temp_v0, f32 *, 0x60);
    M2C_FIELD(arg0, f32 *, 0x84) = (f32) M2C_FIELD(temp_v0, f32 *, 0x64);
    temp_v1 = M2C_FIELD(temp_v0, void **, 0x18);
    M2C_FIELD(arg0, u16 *, 0x72) = (u16) M2C_FIELD(temp_v1, u16 *, 0x14);
    M2C_FIELD(arg0, u16 *, 0x74) = (u16) M2C_FIELD(temp_v1, u16 *, 0x16);
    M2C_FIELD(arg0, u16 *, 0x76) = (u16) M2C_FIELD(temp_v1, u16 *, 0x18);
    M2C_FIELD(arg1, f32 *, 0x88) = (f32) M2C_FIELD(arg0, f32 *, 0x88);
    M2C_FIELD(arg1, f32 *, 0x8C) = (f32) M2C_FIELD(arg0, f32 *, 0x8C);
    M2C_FIELD(arg1, f32 *, 0x90) = (f32) M2C_FIELD(arg0, f32 *, 0x90);
}
