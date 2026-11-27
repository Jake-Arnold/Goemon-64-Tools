#include "m2c_types.h"
f32 __cosf(f32);
extern f64 D_8007A8D0_7B4D0;

f32 func_80003D28_4928(u16 arg0) {
    { *(volatile int *)0x80000000 = 1; } return __cosf((f32) ((f64) ((f32) arg0 / 32768.0f) * D_8007A8D0_7B4D0));
}
