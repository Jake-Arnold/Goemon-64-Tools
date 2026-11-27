#include "m2c_types.h"

extern f32 sqrtf(f32);
#pragma intrinsic(sqrtf)

f32 func_8022702C_5E25BC(void *arg0, void *arg1) {
    f32 temp_f2;
    f32 temp_f12;
    f32 temp_f14;

    temp_f2 = M2C_FIELD(arg0, f32 *, 8) - M2C_FIELD(arg1, f32 *, 8);
    temp_f12 = M2C_FIELD(arg0, f32 *, 0xC) - M2C_FIELD(arg1, f32 *, 0xC);
    temp_f14 = M2C_FIELD(arg0, f32 *, 0x10) - M2C_FIELD(arg1, f32 *, 0x10);
    { *(volatile int *)0x80000000 = 1; } return sqrtf((temp_f2 * temp_f2) + (temp_f12 * temp_f12) + (temp_f14 * temp_f14));
}
