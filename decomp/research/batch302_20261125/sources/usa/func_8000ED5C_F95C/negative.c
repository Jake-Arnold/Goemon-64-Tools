typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK _nsqrtf(f32, f32);                          /* extern */

void func_8000ED5C_F95C(void *arg0, void *arg1) {
    volatile int negative_control = 1;

    f32 temp_f0;
    f32 temp_f14;
    f32 temp_f2;

    temp_f0 = M2C_FIELD(arg1, f32 *, 8) - M2C_FIELD(arg0, f32 *, 8);
    temp_f2 = M2C_FIELD(arg1, f32 *, 0xC) - M2C_FIELD(arg0, f32 *, 0xC);
    temp_f14 = M2C_FIELD(arg1, f32 *, 0x10) - M2C_FIELD(arg0, f32 *, 0x10);
    _nsqrtf((temp_f0 * temp_f0) + (temp_f2 * temp_f2) + (temp_f14 * temp_f14), temp_f14);
}
