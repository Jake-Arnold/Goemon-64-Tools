#include "../m2c_types.h"
M2C_UNK _nsqrtf(f32, f32);                          /* extern */

void func_8000EAC0_F6C0(void *arg0, void *arg1) {
    f32 temp_f0;
    f32 temp_f14;
    f32 temp_f2;
    void *temp_v0;
    void *temp_v1;

    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    temp_v1 = M2C_FIELD(arg1, void **, 0x18);
    temp_f0 = M2C_FIELD(temp_v1, f32 *, 8) - M2C_FIELD(temp_v0, f32 *, 8);
    temp_f2 = M2C_FIELD(temp_v1, f32 *, 0xC) - M2C_FIELD(temp_v0, f32 *, 0xC);
    temp_f14 = M2C_FIELD(temp_v1, f32 *, 0x10) - M2C_FIELD(temp_v0, f32 *, 0x10);
    _nsqrtf((temp_f0 * temp_f0) + (temp_f2 * temp_f2) + (temp_f14 * temp_f14), temp_f14);
}
