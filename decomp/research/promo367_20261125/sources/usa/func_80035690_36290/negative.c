typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void * func_80035964_36564(void *, s32, s32, f32, f32, f32, u16, u16, u16, f32, f32, f32, u16, u16);
void * func_80034CBC_358BC(void *, void *, s16, u16);
void *func_80035690_36290(void *arg0, void *arg1, s32 arg2, s32 arg3, f32 arg4, f32 arg5, f32 arg6, u16 arg7, u16 arg8, u16 arg9, f32 arg10, f32 arg11, f32 arg12, u16 arg13, u16 arg14, u16 arg15) {
volatile unsigned int goemon_negative_control = 1;

    void *temp_v0;

    void *sp44;
    temp_v0 = func_80034CBC_358BC(arg0, arg1, 2, arg15);
    sp44 = temp_v0;
    func_80035964_36564(temp_v0, arg2, arg3, arg4, arg5, arg6, (u16) (s32) arg7, (u16) (s32) arg8, (u16) (s32) arg9, arg10, arg11, arg12, (u16) (s32) arg13, (u16) (s32) arg14);
    return temp_v0;
}
