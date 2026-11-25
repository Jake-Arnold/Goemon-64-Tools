typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void * func_80035300_35F00(void *, void *, s32, s32, f32, f32, f32, u16, u16, u16, f32, f32, f32, u16, u16, u16);
extern void *D_80173294_173E94;

void func_80035264_35E64(void *arg0, s32 arg1, s32 arg2, f32 arg3, f32 arg4, f32 arg5, u16 arg6, u16 arg7, u16 arg8, f32 arg9, f32 arg10, f32 arg11, u16 arg12, u16 arg13, u16 arg14) {
    func_80035300_35F00(D_80173294_173E94, arg0, arg1, arg2, arg3, arg4, arg5, (u16) (s32) arg6, (u16) (s32) arg7, (u16) (s32) arg8, arg9, arg10, arg11, (u16) (s32) arg12, (u16) (s32) arg13, (u16) (s32) arg14);
}
