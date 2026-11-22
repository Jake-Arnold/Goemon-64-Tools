#include "../m2c_types.h"
void func_080013C8_706A68(void *arg0) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    M2C_FIELD(arg0, f32 *, 0x78) = (f32) M2C_FIELD(temp_v0, f32 *, 8);
    M2C_FIELD(arg0, f32 *, 0x7C) = (f32) M2C_FIELD(temp_v0, f32 *, 0xC);
    M2C_FIELD(arg0, f32 *, 0x80) = (f32) M2C_FIELD(temp_v0, f32 *, 0x10);
    M2C_FIELD(arg0, s16 *, 0xE4) = (s16) (M2C_FIELD(temp_v0, u16 *, 0x14) & 0x3FF);
    M2C_FIELD(arg0, s16 *, 0xE6) = (s16) (M2C_FIELD(temp_v0, u16 *, 0x16) & 0x3FF);
    M2C_FIELD(arg0, s16 *, 0xE8) = (s16) (M2C_FIELD(temp_v0, u16 *, 0x18) & 0x3FF);
}
