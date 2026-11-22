#include "../m2c_types.h"
void func_8022398C_5DEF1C(void *arg0, f32 arg1, f32 arg2, f32 arg3, s32 arg4) {
    f32 temp_f0;
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    temp_f0 = (f32) arg4;
    M2C_FIELD(arg0, f32 *, 0x78) = (f32) ((arg1 - M2C_FIELD(temp_v0, f32 *, 8)) / temp_f0);
    M2C_FIELD(arg0, f32 *, 0x7C) = (f32) ((arg2 - M2C_FIELD(temp_v0, f32 *, 0xC)) / temp_f0);
    M2C_FIELD(arg0, f32 *, 0x80) = (f32) ((arg3 - M2C_FIELD(temp_v0, f32 *, 0x10)) / temp_f0);
}
