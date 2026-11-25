typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80022500_23100(s32, s32, s32, s32, s32, s32, void *);
void func_80022DF4_239F4(s32 arg0, s32 arg1, s32 arg2, s32 arg3, s32 arg4, s32 arg5, void *arg6) {
    s16 temp_v0;
    s32 temp_f6;
    s32 temp_v0_2;

    temp_v0 = M2C_FIELD(arg6, s16 *, 0x10);
    temp_f6 = (s32) M2C_FIELD(arg6, f32 *, 0x24);
    if (temp_v0 < (temp_f6 + arg2)) {
        func_80022500_23100(arg0, arg1, arg2, arg3, temp_v0 - arg2, arg5, arg6);
        temp_v0_2 = M2C_FIELD(arg6, s16 *, 0x10) - arg2;
        func_80022500_23100(temp_v0_2 + arg0, arg1, 0, arg3, arg4 - temp_v0_2, arg5, arg6);
        return;
    }
    func_80022500_23100(arg0, arg1, arg2, arg3, temp_f6, arg5, arg6);
}
