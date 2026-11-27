#include "m2c_types.h"
f32 func_801D1628_63FB18(f32, f32);

void func_801D1898_63FD88(void *arg0) {
    f32 temp_f0;
    f32 temp_f12;
    f32 var_f2;

    temp_f12 = M2C_FIELD(arg0, f32 *, 0x338) + M2C_FIELD(arg0, f32 *, 0x320);
    M2C_FIELD(arg0, f32 *, 0x378) = temp_f12;
    temp_f0 = func_801D1628_63FB18(temp_f12, 0.0f);
    var_f2 = temp_f0;
    if (temp_f0 < 0.0f) {
        var_f2 = 0.0f;
    }
    M2C_FIELD(arg0, f32 *, 0x374) = M2C_FIELD(arg0, f32 *, 0x334) + var_f2;
    M2C_FIELD(arg0, f32 *, 0x370) = 148.0f;

    *(volatile s32 *)0x80000000 = 1;
}
