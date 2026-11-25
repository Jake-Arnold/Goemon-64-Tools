#include "m2c_types.h"
extern char func_80034ED4_35AD4;
extern f64 D_080057D0_6EE920;

void func_08003750_6EC8A0(s32 arg0, void *arg1) {
    M2C_FIELD(arg1, f32 *, 8) = (f32) ((f64) M2C_FIELD(arg1, f32 *, 8) - D_080057D0_6EE920);
    if (M2C_FIELD(arg1, f32 *, 8) < -175.0f) {
        ((M2C_UNK(*)())&func_80034ED4_35AD4)();
    }
}
