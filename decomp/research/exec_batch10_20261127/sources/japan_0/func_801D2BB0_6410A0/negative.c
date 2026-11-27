#include "m2c_types.h"

void func_800039C4_45C4(f32, f32);
f32 func_801D13C4_63F8B4(f32, f32);

void func_801D2BB0_6410A0(f32 arg0, f32 arg1) {
    f32 x0;
    f32 x1;

    x0 = func_801D13C4_63F8B4(arg0, 0.0f);
    if (x0 < 0.0f) {
        x0 = 0.0f;
    }
    x1 = func_801D13C4_63F8B4(arg1, 0.0f);
    if (x1 < 0.0f) {
        x1 = 0.0f;
    }
    func_800039C4_45C4(x1 - x0, arg1 - arg0);

    *(volatile s32 *)0x80000000 = 1;
}
