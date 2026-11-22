#include "m2c_types.h"
void func_80217938_69F038(void *arg0, f32 arg1) {
    f32 temp_f0;
    f32 var_f2;
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x5C);
    M2C_FIELD(temp_v0, f32 *, 0x4C) = arg1;
    temp_f0 = M2C_FIELD(M2C_FIELD(temp_v0, void **, 0x54), f32 *, 0x24);
    if (arg1 < temp_f0) {
        var_f2 = -(M2C_FIELD(temp_v0, f32 *, 0x4C) - temp_f0);
    } else {
        var_f2 = M2C_FIELD(temp_v0, f32 *, 0x4C) - temp_f0;
    }
    M2C_FIELD(temp_v0, f32 *, 0x50) = (f32) (var_f2 / M2C_FIELD(temp_v0, f32 *, 8));
}
