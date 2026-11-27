#include "m2c_types.h"
f32 func_801CBEF8_63AD48(f32, f32);

void func_801CC168_63AFB8(void *arg0) {
    f32 temp_f0;
    f32 temp_f12;
    f32 var_f2;

    temp_f12 = M2C_FIELD(arg0, f32 *, 0x338) + M2C_FIELD(arg0, f32 *, 0x320);
    M2C_FIELD(arg0, f32 *, 0x378) = temp_f12;
    temp_f0 = func_801CBEF8_63AD48(temp_f12, 0.0f);
    var_f2 = temp_f0;
    if (temp_f0 < 0.0f) {
        var_f2 = 0.0f;
    }
    M2C_FIELD(arg0, f32 *, 0x374) = M2C_FIELD(arg0, f32 *, 0x334) + var_f2;
    M2C_FIELD(arg0, f32 *, 0x370) = 148.0f;
}
