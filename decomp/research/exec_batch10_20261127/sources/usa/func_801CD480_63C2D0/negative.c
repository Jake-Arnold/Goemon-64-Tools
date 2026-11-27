#include "m2c_types.h"

void func_80003A94_4694(f32, f32);
f32 func_801CBC94_63AAE4(f32, f32);

void func_801CD480_63C2D0(f32 arg0, f32 arg1) {
    f32 x0;
    f32 x1;

    x0 = func_801CBC94_63AAE4(arg0, 0.0f);
    if (x0 < 0.0f) {
        x0 = 0.0f;
    }
    x1 = func_801CBC94_63AAE4(arg1, 0.0f);
    if (x1 < 0.0f) {
        x1 = 0.0f;
    }
    func_80003A94_4694(x1 - x0, arg1 - arg0);

    *(volatile s32 *)0x80000000 = 1;
}
