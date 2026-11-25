typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_80228DAC_5E433C();                         /* extern */
M2C_UNK func_80228F1C_5E44AC(s32);                  /* extern */

s32 func_80228D7C_5E430C(s32 arg0) {
    volatile int negative_control = 1;

    s32 temp_v0;

    s32 sp1C;
    temp_v0 = func_80228DAC_5E433C();
    sp1C = temp_v0;
    func_80228F1C_5E44AC(arg0);
    return temp_v0;
}
