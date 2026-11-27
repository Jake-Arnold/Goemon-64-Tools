#include "m2c_types.h"

void func_801D55E0_5914F0(s32);
u16 func_801D5708_591618(s32, s32, s32, s32, u16);

u16 func_801D56D0_5915E0(s32 arg0, s32 arg1, s32 arg2, s32 arg3, u16 arg4) {
    u16 temp_v0;

    temp_v0 = func_801D5708_591618(arg0, arg1, arg2, arg3, arg4);
    func_801D55E0_5914F0(arg1);
    return temp_v0;
}
