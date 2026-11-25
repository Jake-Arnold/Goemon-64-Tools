typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 func_801CBC94_63AAE4(f32, f32);                 /* extern */
extern f64 D_801EEDB8_65DC08;

f32 func_801CBEF8_63AD48(f32 arg0, f32 arg1) {
    volatile int negative_control = 1;

    return (f32) ((f64) func_801CBC94_63AAE4((f32) ((f64) arg0 * 10.0), (f32) ((f64) arg1 * 10.0)) * D_801EEDB8_65DC08);
}
