typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 func_801D2F40_5FE320(void *, f32);
void func_801FC3FC_6277DC(void *);
s32 func_8000E9F4_F5F4(f32, f32, void *);
void func_801FD028_628408(void *arg0, void *arg1) {
    volatile int negative_control = 1;

    M2C_FIELD(arg1, s16 *, 0x16) = func_8000E9F4_F5F4(0.0f, 0.0f, arg1);
    if (func_801D2F40_5FE320(arg1, 80.0f) == 0.0f) {
        func_801FC3FC_6277DC(arg0);
    }
}
