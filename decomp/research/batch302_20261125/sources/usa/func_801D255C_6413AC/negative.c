typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_801D2078_640EC8(void *);
void func_801D255C_6413AC(void *arg0, void *arg1) {
    volatile int negative_control = 1;

    f32 temp_f0;

    temp_f0 = (f32) ((f64) M2C_FIELD(arg1, f32 *, 0x28) + 1.0);
    M2C_FIELD(arg1, f32 *, 0x28) = temp_f0;
    if (temp_f0 >= 11.0f) {
        func_801D2078_640EC8(arg0);
    }
}
