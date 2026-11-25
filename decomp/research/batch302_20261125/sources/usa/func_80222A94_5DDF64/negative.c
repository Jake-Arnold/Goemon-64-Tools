typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 __cosf(f32);                                    /* extern */
f32 __sinf(f32);                                    /* extern */

void func_80222A94_5DDF64(f32 arg0, f32 arg1, f32 arg2, f32 *arg3, f32 *arg4) {
    volatile int negative_control = 1;

    f32 sp1C;

    sp1C = __cosf(arg2);
    *arg3 = (__sinf(arg2) * arg1) + (sp1C * arg0);
    sp1C = __sinf(arg2);
    *arg4 = (__cosf(arg2) * arg1) + (-sp1C * arg0);
}
