#include "../m2c_types.h"
extern char func_8003521C_35E1C;
M2C_UNK func_08004FEC_6F84CC();                     /* static */

void func_08004F8C_6F846C(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x250;
    M2C_FIELD(arg0, s32 *, 0x60) = 0x80000020;
    M2C_FIELD(arg0, s32 *, 0x64) = 2;
    M2C_FIELD(arg0, s8 *, 0x6C) = 2;
    M2C_FIELD(arg1, f32 *, 0x1C) = 1.0f;
    M2C_FIELD(arg1, f32 *, 0x20) = 1.0f;
    M2C_FIELD(arg1, f32 *, 0x24) = 1.0f;
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08004FEC_6F84CC);
}
