#include "../m2c_types.h"
void func_08000804_7406D4(void *arg0) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, s32 *, 0xD4);
    M2C_FIELD(arg0, s32 *, 0xDC) = temp_v0;
    M2C_FIELD(arg0, f32 *, 0xE4) = (f32) (M2C_FIELD(arg0, f32 *, 0xE0) / (f32) temp_v0);
}
