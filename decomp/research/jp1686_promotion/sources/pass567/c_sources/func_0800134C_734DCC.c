#include "../m2c_types.h"
void func_0800134C_734DCC(void *arg0, f32 arg1, f32 arg2, f32 arg3, f32 arg4) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0xD0);
    M2C_FIELD(temp_v0, s32 *, 0x10) = 1;
    M2C_FIELD(temp_v0, f32 *, 0x14) = arg1;
    M2C_FIELD(temp_v0, f32 *, 0x18) = arg2;
    M2C_FIELD(temp_v0, f32 *, 0x1C) = arg3;
    M2C_FIELD(temp_v0, f32 *, 0x20) = arg4;
}
