#include "m2c_types.h"
f32 func_8001B13C_1BD3C(void *);                    /* extern */

void func_80217EE0_6815D0(void *arg0, void *arg1) {
    if (M2C_FIELD(arg0, u8 *, 0x5C) == 0) {
        M2C_FIELD(arg1, s16 *, 0x16) = 0x200;
    }
    M2C_FIELD(arg1, f32 *, 0x28) = (f32) ((f64) M2C_FIELD(arg1, f32 *, 0x28) + 0.25);
    if ((func_8001B13C_1BD3C(arg1) - 1.0f) < M2C_FIELD(arg1, f32 *, 0x28)) {
        M2C_FIELD(arg1, f32 *, 0x28) = 0.0f;
    }
}
