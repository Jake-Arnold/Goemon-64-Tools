#include "m2c_types.h"
extern f64 D_8021C8E0_67B750;

s32 func_80219A9C_67890C(void *arg0) {
    if (D_8021C8E0_67B750 < (f64) M2C_FIELD(arg0, f32 *, 0xB0)) {
        return 1;
    }
    return 0;
}
