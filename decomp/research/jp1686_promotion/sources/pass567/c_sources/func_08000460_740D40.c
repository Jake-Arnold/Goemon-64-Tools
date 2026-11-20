#include "../m2c_types.h"
void func_08000460_740D40(void *arg0, f32 arg1, f32 arg2, f32 arg3, f32 arg4) {
    M2C_FIELD(arg0, s8 *, 0xD2) = 1;
    M2C_FIELD(arg0, f32 *, 0xD4) = arg1;
    M2C_FIELD(arg0, f32 *, 0xD8) = arg2;
    M2C_FIELD(arg0, f32 *, 0xDC) = arg3;
    M2C_FIELD(arg0, f32 *, 0xE0) = arg4;
}
