#include "m2c_types.h"
s32 func_801F236C_5AE27C(f32 arg0, f32 *arg1) {
    f32 *var_v0;
    f32 temp_f0;
    s32 var_v1;
    f32 zero;

    zero = 0.0f;
    var_v1 = 0;
    var_v0 = arg1;
    do {
        temp_f0 = *var_v0;
        if (zero == temp_f0) {
            return var_v1;
        }
        if (arg0 < temp_f0) {
            return var_v1;
        }
        var_v1 += 1;
        var_v0 += 1;
    } while (var_v1 != 3);
    return -1;
}
