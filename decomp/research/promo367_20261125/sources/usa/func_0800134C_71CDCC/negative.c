#include "m2c_types.h"
extern char func_80034ED4_35AD4;

void func_0800134C_71CDCC(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v0;

    M2C_FIELD(arg1, f32 *, 0xC) = (f32) (M2C_FIELD(arg1, f32 *, 0xC) + 1.0f);
    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        ((M2C_UNK(*)())&func_80034ED4_35AD4)();
    }
}
