#include "../m2c_types.h"
extern f64 D_8021C8F8_67B768;
extern f64 D_8021C900_67B770;

void func_8021A7F0_679660(s32 arg0, f32 *arg1, f32 *arg2, f32 *arg3) {
    f64 temp_f0;

    temp_f0 = (f64) arg0 + 0.5;
    *arg1 = (f32) (15.0 - (temp_f0 * 10.0));
    *arg2 = (f32) (temp_f0 * D_8021C8F8_67B768);
    *arg3 = (f32) (temp_f0 * D_8021C900_67B770);
}
