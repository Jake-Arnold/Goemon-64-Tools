#include "m2c_types.h"
extern void func_80012628_13228(s32, f32, f32);

void func_0800260C_6B1A1C(s32 arg0, f32 arg1, f32 arg2, s32 arg3) {
    void (*fn)(s32, f32, f32) = func_80012628_13228;
    fn(arg0, arg1, arg2);

    *(volatile s32 *)0x80000000 = 1;
}
