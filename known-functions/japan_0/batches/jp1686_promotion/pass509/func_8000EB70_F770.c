#include "m2c_types.h"
M2C_UNK _nsqrtf(f32);                               /* extern */

void func_8000EB70_F770(void *arg0, void *arg1) {
    f32 temp_f0;
    f32 temp_f2;

    temp_f0 = M2C_FIELD(arg1, f32 *, 8) - M2C_FIELD(arg0, f32 *, 8);
    temp_f2 = M2C_FIELD(arg1, f32 *, 0x10) - M2C_FIELD(arg0, f32 *, 0x10);
    _nsqrtf((temp_f0 * temp_f0) + (temp_f2 * temp_f2));
}
