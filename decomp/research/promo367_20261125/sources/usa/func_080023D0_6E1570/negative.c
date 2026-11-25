#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern M2C_UNK func_08002444_6E15E4;

void func_080023D0_6E1570(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v0;

    M2C_FIELD(arg1, u16 *, 0x14) = (u16) ((M2C_FIELD(arg1, u16 *, 0x14) - 4) & 0x3FF);
    M2C_FIELD(arg1, u16 *, 0x16) = (u16) (M2C_FIELD(arg1, u16 *, 0x16) + 0x10);
    M2C_FIELD(arg1, u16 *, 0x18) = (u16) (M2C_FIELD(arg1, u16 *, 0x18) + 1);
    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, u16 *, 0x8A) = 0x1EU;
        M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08002444_6E15E4);
    }
}
