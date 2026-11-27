#include "m2c_types.h"
extern void func_800121B8_12DB8(s32, f32, f32);

void func_080025F8_6B64F8(s32 arg0, f32 arg1, f32 arg2, s32 arg3) {
    void (*fn)(s32, f32, f32) = func_800121B8_12DB8;
    fn(arg0, arg1, arg2);

    *(volatile s32 *)0x80000000 = 1;
}
