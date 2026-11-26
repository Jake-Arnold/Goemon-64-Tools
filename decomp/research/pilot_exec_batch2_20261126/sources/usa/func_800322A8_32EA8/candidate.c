#include "m2c_types.h"
void func_80032320_32F20(void *, s32, f32);

void func_800322A8_32EA8(void *arg0, f32 arg1, f32 arg2, f32 arg3, f32 arg4, f32 arg5, f32 arg6, f32 arg7) {
    M2C_FIELD(arg0, f32 *, 0) = arg1;
    M2C_FIELD(arg0, f32 *, 4) = arg2;
    M2C_FIELD(arg0, f32 *, 8) = arg3;
    M2C_FIELD(arg0, f32 *, 0xC) = arg4;
    M2C_FIELD(arg0, f32 *, 0x10) = arg5;
    M2C_FIELD(arg0, f32 *, 0x14) = arg6;
    func_80032320_32F20(arg0, 1, arg7 + 2.0f);
}
