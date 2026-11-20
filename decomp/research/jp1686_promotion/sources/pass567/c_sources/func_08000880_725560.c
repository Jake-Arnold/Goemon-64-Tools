#include "../m2c_types.h"
void func_08000880_725560(void *arg0, f32 arg1, f32 arg2, f32 arg3, u16 arg4, u16 arg5, u16 arg6) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    M2C_FIELD(temp_v0, f32 *, 8) = arg1;
    M2C_FIELD(temp_v0, f32 *, 0xC) = arg2;
    M2C_FIELD(temp_v0, f32 *, 0x10) = arg3;
    M2C_FIELD(temp_v0, u16 *, 0x14) = arg4;
    M2C_FIELD(temp_v0, u16 *, 0x16) = arg5;
    M2C_FIELD(temp_v0, u16 *, 0x18) = arg6;
}
