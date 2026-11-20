#include "../m2c_types.h"
void func_08001634_738914(void *arg0, s32 arg1) {
    f32 temp_f0;
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, s32 *, 0xD4);
    temp_f0 = (f32) arg1;
    M2C_FIELD(arg0, s32 *, 0xDC) = temp_v0;
    M2C_FIELD(arg0, f32 *, 0xE0) = temp_f0;
    M2C_FIELD(arg0, f32 *, 0xE4) = (f32) (temp_f0 / (f32) temp_v0);
}
