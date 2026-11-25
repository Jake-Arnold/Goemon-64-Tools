#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern char func_8021DB3C_5D90CC;
extern char func_8021E024_5D95B4;
extern u16 D_80162420_163020;
extern M2C_UNK func_080022B0_6E0A40;

void func_080021C8_6E0958(void *arg0, void *arg1) {
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    if (M2C_FIELD(arg0, u8 *, 0xD8) != 0) {
        ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, (void *)2, 0x3F000000, 4);
    } else {
        ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 2, 0x3E800000, 4);
    }
    ((M2C_UNK(*)())&func_8021DB3C_5D90CC)(arg0, 3);
    M2C_FIELD(arg1, f32 *, 0x28) = (f32) M2C_FIELD(arg0, f32 *, 0xD0);
    if (D_80162420_163020 & 1) {
        M2C_FIELD(arg0, s16 *, 0xDA) = (s16) (((s32(*)())&func_8021E024_5D95B4)(0xA) + 1);
    } else {
        M2C_FIELD(arg0, s16 *, 0xDA) = 0;
    }
    M2C_FIELD(arg0, s16 *, 0x8A) = 0;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_080022B0_6E0A40);
}
