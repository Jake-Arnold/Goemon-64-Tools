typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_801E5328_654178(s32, M2C_UNK, f32 *, f32 *, f32 *, void *, void *, void *, f32);
void func_801E5C74_654AC4(s32 arg0, s32 arg1, void *arg2, void *arg3, void *arg4, f32 *arg5, f32 *arg6, f32 *arg7, f32 arg8) {
volatile unsigned int goemon_negative_control = 1;

    func_801E5328_654178(arg0, arg1, arg5, arg6, arg7, arg2, arg3, arg4, arg8);
}
