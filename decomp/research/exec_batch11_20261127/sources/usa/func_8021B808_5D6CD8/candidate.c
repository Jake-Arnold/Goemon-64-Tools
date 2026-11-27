#include "m2c_types.h"

void func_8021B808_5D6CD8(void *arg0) {
    f32 scale = 2.0f;
    if (M2C_FIELD(arg0, s32 *, 0x60) & 0x200) {
        void *temp_v0 = M2C_FIELD(arg0, void **, 0x18);
        M2C_FIELD(temp_v0, f32 *, 8) += M2C_FIELD(arg0, f32 *, 0x78) * scale;
        M2C_FIELD(temp_v0, f32 *, 0xC) += M2C_FIELD(arg0, f32 *, 0x7C) * scale;
        M2C_FIELD(temp_v0, f32 *, 0x10) += M2C_FIELD(arg0, f32 *, 0x80) * scale;
    }
}
