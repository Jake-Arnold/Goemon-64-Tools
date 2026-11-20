#include "m2c_types.h"
extern f64 D_08003218_6F7B38;

s32 func_080017A4_6F60C4(void *arg0) {
    if (D_08003218_6F7B38 < (f64) M2C_FIELD(arg0, f32 *, 0xDC)) {
        return 1;
    }
    return 0;
}
