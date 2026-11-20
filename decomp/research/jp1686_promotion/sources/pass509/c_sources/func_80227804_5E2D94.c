#include "m2c_types.h"
f32 __cosf(f32);                                    /* extern */
f32 __sinf(f32);                                    /* extern */

void func_80227804_5E2D94(f32 arg0, f32 arg1, f32 arg2, f32 *arg3, f32 *arg4) {
    f32 sp1C;

    sp1C = __cosf(arg2);
    *arg3 = (__sinf(arg2) * arg1) + (sp1C * arg0);
    sp1C = __sinf(arg2);
    *arg4 = (__cosf(arg2) * arg1) + (-sp1C * arg0);
}
