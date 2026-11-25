#include "../m2c_types.h"
extern char func_8003521C_35E1C;
M2C_UNK func_08003A8C_6E2C2C();                     /* static */

void func_08003A40_6E2BE0(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    M2C_FIELD(arg0, s16 *, 0x8A) = 0x3C;
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08003A8C_6E2C2C);
}
