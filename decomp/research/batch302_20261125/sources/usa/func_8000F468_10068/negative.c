typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8000F420_10020(u16, s32, void *, s32); /* extern */
f32 func_8001CC38_1D838(s32, s32, s32, s32, f32 *, f32 *); /* extern */

void func_8000F468_10068(u16 arg0, s32 arg1, void *arg2, s32 arg3) {
    volatile int negative_control = 1;

    f32 sp24;
    f32 sp20;

    if ((func_8001CC38_1D838(arg1, M2C_FIELD(arg2, s32 *, 8), M2C_FIELD(arg2, s32 *, 0xC), M2C_FIELD(arg2, s32 *, 0x10), &sp24, &sp20) >= 0.0f) && !(sp24 < 0.0f) && !(sp24 > 320.0f) && !(sp20 < 0.0f) && !(sp20 > 240.0f)) {
        func_8000F420_10020(arg0, arg1, arg2, arg3);
    }
}
