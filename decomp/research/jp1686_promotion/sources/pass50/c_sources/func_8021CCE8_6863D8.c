#include "m2c_types.h"
f32 func_8001B13C_1BD3C(void *);                    /* extern */

void func_8021CCE8_6863D8(void *arg0, void *arg1) {
    f32 temp_f2;

    M2C_FIELD(arg1, f32 *, 0x28) = (f32) (M2C_FIELD(arg0, f32 *, 0x60) + M2C_FIELD(arg1, f32 *, 0x28));
    temp_f2 = func_8001B13C_1BD3C(arg1) - 1.0f;
    if (temp_f2 < M2C_FIELD(arg1, f32 *, 0x28)) {
        if (M2C_FIELD(arg0, u8 *, 0x5D) == 1) {
            M2C_FIELD(arg1, f32 *, 0x28) = 0.0f;
            return;
        }
        M2C_FIELD(arg1, f32 *, 0x28) = temp_f2;
    }
}
