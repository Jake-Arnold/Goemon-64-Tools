typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_8000FBDC_107DC(u16, void *, f32, f32, f32, f32);
void func_8000F4A8_100A8(u16 arg0, void *arg1, f32 arg2, f32 arg3, f32 arg4, f32 arg5) {
    func_8000FBDC_107DC(arg0, arg1, arg2, arg3, arg4, arg5);
}
