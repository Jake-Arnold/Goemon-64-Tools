typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_08000938_706728(void *arg0, f32 arg1, u16 arg2, f32 arg3, f32 arg4, f32 arg5, f32 arg6) {
    volatile int negative_control = 1;

    M2C_FIELD(arg0, s16 *, 0xD2) = arg2;
    M2C_FIELD(arg0, f32 *, 0xDC) = arg1;
    M2C_FIELD(arg0, s16 *, 0xD4) = (s16) (s32) arg5;
    M2C_FIELD(arg0, f32 *, 0xD8) = arg3;
    M2C_FIELD(arg0, f32 *, 0xE0) = arg4;
    M2C_FIELD(arg0, s16 *, 0xD6) = (s16) (s32) arg6;
}
