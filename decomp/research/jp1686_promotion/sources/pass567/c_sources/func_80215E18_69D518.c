#include "../m2c_types.h"
void func_80215E18_69D518(void *arg0, s32 arg1) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, s32 *, 0x5C);
    M2C_FIELD(arg0, s32 *, 0x78) = arg1;
    M2C_FIELD(arg0, s32 *, 0x7C) = temp_v0;
    M2C_FIELD(arg0, f32 *, 0x84) = (f32) (((f32) arg1 - M2C_FIELD(arg0, f32 *, 0x80)) / (f32) temp_v0);
}
