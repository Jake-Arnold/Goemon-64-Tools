typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
typedef struct { f32 f_0; f32 f_4; } Recovered_arg0;
typedef struct { f32 f_0; f32 f_4; } Recovered_arg2;
typedef struct { f32 f_0; f32 f_4; f32 f_8; f32 f_C; } Recovered_arg1;
void func_80222A48_5DDF18(Recovered_arg0 *arg0, Recovered_arg1 *arg1, Recovered_arg2 *arg2) {
    volatile int negative_control = 1;

    arg0->f_0 = (f32) ((arg2->f_4 * arg1->f_4) + (arg1->f_0 * arg2->f_0));
    arg0->f_4 = (f32) ((arg2->f_4 * arg1->f_C) + (arg1->f_8 * arg2->f_0));
}
