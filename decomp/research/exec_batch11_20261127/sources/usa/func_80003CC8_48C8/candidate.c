#include "m2c_types.h"
f32 __sinf(f32);
extern f64 D_8007A8C8_7B4C8;

f32 func_80003CC8_48C8(u16 arg0) {
    return __sinf((f32) ((f64) ((f32) arg0 / 32768.0f) * D_8007A8C8_7B4C8));
}
