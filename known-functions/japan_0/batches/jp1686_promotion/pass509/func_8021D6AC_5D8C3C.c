#include "m2c_types.h"
extern M2C_UNK D_80162420_163020;

void func_8021D6AC_5D8C3C(void *arg0) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    if (M2C_FIELD(arg0, s32 *, 0x60) & 0x10000000) {
        M2C_FIELD(&D_80162420_163020, f32 *, 0x74) = (f32) M2C_FIELD(temp_v0, f32 *, 8);
        M2C_FIELD(&D_80162420_163020, f32 *, 0x78) = (f32) M2C_FIELD(temp_v0, f32 *, 0xC);
        M2C_FIELD(&D_80162420_163020, f32 *, 0x7C) = (f32) M2C_FIELD(temp_v0, f32 *, 0x10);
        M2C_FIELD(&D_80162420_163020, f32 *, 0x80) = (f32) M2C_FIELD(arg0, f32 *, 0x78);
        M2C_FIELD(&D_80162420_163020, f32 *, 0x84) = (f32) M2C_FIELD(arg0, f32 *, 0x7C);
        M2C_FIELD(&D_80162420_163020, f32 *, 0x88) = (f32) M2C_FIELD(arg0, f32 *, 0x80);
    }
}
