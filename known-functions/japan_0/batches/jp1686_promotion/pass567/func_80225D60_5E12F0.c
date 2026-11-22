#include "../m2c_types.h"
extern M2C_UNK D_80162420_163020;

void func_80225D60_5E12F0(void *arg0) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    M2C_FIELD(arg0, s32 *, 0xB4) = (s32) M2C_FIELD(arg0, s32 *, 0xC);
    M2C_FIELD(&D_80162420_163020, u16 *, 0x14E) = (u16) M2C_FIELD(temp_v0, u16 *, 0x16);
    M2C_FIELD(&D_80162420_163020, s32 *, 0x150) = (s32) M2C_FIELD(temp_v0, s32 *, 0x2C);
    M2C_FIELD(&D_80162420_163020, u16 *, 0x154) = (u16) M2C_FIELD(temp_v0, u16 *, 0x7E);
    M2C_FIELD(&D_80162420_163020, s16 *, 0x156) = (s16) M2C_FIELD(temp_v0, u8 *, 0x7C);
}
