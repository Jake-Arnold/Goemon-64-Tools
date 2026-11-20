#include "m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08000180_6B4080();                     /* static */
extern M2C_UNK D_801624C8_1630C8;
extern s32 D_801CD050_1CDC50;
extern s32 D_801CD05C_1CDC5C;

void func_080000EC_6B3FEC(void *arg0, void *arg1) {
    M2C_FIELD(arg1, f32 *, 8) = (f32) M2C_FIELD(arg0, f32 *, 0xDC);
    M2C_FIELD(arg1, f32 *, 0xC) = (f32) M2C_FIELD(arg0, f32 *, 0xE0);
    M2C_FIELD(arg1, f32 *, 0x10) = (f32) M2C_FIELD(arg0, f32 *, 0xE4);
    M2C_FIELD(arg1, u16 *, 0x14) = (u16) M2C_FIELD(arg0, u16 *, 0xE8);
    M2C_FIELD(arg1, u16 *, 0x16) = (u16) M2C_FIELD(arg0, u16 *, 0xEA);
    M2C_FIELD(arg1, u16 *, 0x18) = (u16) M2C_FIELD(arg0, u16 *, 0xEC);
    if ((D_801CD050_1CDC50 != 0) && (M2C_FIELD(&D_801624C8_1630C8, s32 *, 0x10C) != 0) && (M2C_FIELD(&D_801624C8_1630C8, s32 *, 0x10C) != 2) && (D_801CD05C_1CDC5C == M2C_FIELD(arg0, u8 *, 0xDB))) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000180_6B4080);
    }
}
