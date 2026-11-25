#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern s32 D_8015CDE4;
extern s32 D_801C7920_1C8520;
extern s32 D_801C792C_1C852C;
extern M2C_UNK func_08000180_6AF590;

void func_080000EC_6AF4FC(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    M2C_FIELD(arg1, f32 *, 8) = (f32) M2C_FIELD(arg0, f32 *, 0xDC);
    M2C_FIELD(arg1, f32 *, 0xC) = (f32) M2C_FIELD(arg0, f32 *, 0xE0);
    M2C_FIELD(arg1, f32 *, 0x10) = (f32) M2C_FIELD(arg0, f32 *, 0xE4);
    M2C_FIELD(arg1, u16 *, 0x14) = (u16) M2C_FIELD(arg0, u16 *, 0xE8);
    M2C_FIELD(arg1, u16 *, 0x16) = (u16) M2C_FIELD(arg0, u16 *, 0xEA);
    M2C_FIELD(arg1, u16 *, 0x18) = (u16) M2C_FIELD(arg0, u16 *, 0xEC);
    if ((D_801C7920_1C8520 != 0) && (D_8015CDE4 != 0) && (D_8015CDE4 != 2) && (D_801C792C_1C852C == M2C_FIELD(arg0, u8 *, 0xDB))) {
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08000180_6AF590);
    }
}
