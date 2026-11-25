#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021927C_5D474C;
extern char func_8021B4FC_5D69CC;
extern M2C_UNK func_08002EB8_6DCD88;

void func_08002E20_6DCCF0(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    if (temp_v0 == 0) {
        ((M2C_UNK(*)())&func_8021927C_5D474C)(arg0);
        ((M2C_UNK(*)())&func_8021B4FC_5D69CC)(arg0);
        M2C_FIELD(arg0, s8 *, 0x75) = 0x14;
        M2C_FIELD(arg0, s16 *, 0x96) = 0xE1;
        M2C_FIELD(arg0, f32 *, 0x7C) = 2.5f;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08002EB8_6DCD88, arg0);
    }
}
