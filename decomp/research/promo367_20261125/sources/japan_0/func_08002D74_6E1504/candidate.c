#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021DFEC_5D957C;
extern char func_8022026C_5DB7FC;
extern M2C_UNK func_08002E0C_6E159C;

void func_08002D74_6E1504(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    if (temp_v0 == 0) {
        ((M2C_UNK(*)())&func_8021DFEC_5D957C)(arg0);
        ((M2C_UNK(*)())&func_8022026C_5DB7FC)(arg0);
        M2C_FIELD(arg0, s8 *, 0x75) = 0x14;
        M2C_FIELD(arg0, s16 *, 0x96) = 0xE1;
        M2C_FIELD(arg0, f32 *, 0x7C) = 2.5f;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08002E0C_6E159C, arg0);
    }
}
