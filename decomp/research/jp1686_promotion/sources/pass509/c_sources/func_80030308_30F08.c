#include "m2c_types.h"
void func_80030308_30F08(f32 *arg0, f32 *arg1, f32 *arg2, f32 *arg3, void *arg4) {
    f32 temp_f0;
    f32 temp_f0_2;

    temp_f0 = M2C_FIELD(arg4, f32 *, 0x18);
    if (temp_f0 > 0.0f) {
        if (*arg0 < temp_f0) {
            *arg0 = temp_f0;
        }
    } else if (temp_f0 < *arg1) {
        *arg1 = temp_f0;
    }
    temp_f0_2 = M2C_FIELD(arg4, f32 *, 0x20);
    if (temp_f0_2 > 0.0f) {
        if (*arg2 < temp_f0_2) {
            *arg2 = temp_f0_2;
        }
    } else if (temp_f0_2 < *arg3) {
        *arg3 = temp_f0_2;
    }
}
