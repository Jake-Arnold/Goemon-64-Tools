#include "../m2c_types.h"
extern char func_8003521C_35E1C;
M2C_UNK func_08001C10_6C1360();                     /* static */

void func_08001BBC_6C130C(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    M2C_FIELD(arg0, s32 *, 0x60) = 0x2006E1;
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    M2C_FIELD(arg1, f32 *, 0xC) = -93.0f;
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08001C10_6C1360);
}
