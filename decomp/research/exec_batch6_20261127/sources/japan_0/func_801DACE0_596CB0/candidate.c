#include "m2c_types.h"

void func_801DABF0_596BC0(s32);
u16 func_801DAD18_596CE8(s32, s32, s32, s32, u16);

u16 func_801DACE0_596CB0(s32 arg0, s32 arg1, s32 arg2, s32 arg3, u16 arg4) {
    u16 temp_v0;

    temp_v0 = func_801DAD18_596CE8(arg0, arg1, arg2, arg3, arg4);
    func_801DABF0_596BC0(arg1);
    return temp_v0;
}
