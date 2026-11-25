typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
typedef struct { f32 f_0; f32 f_4; f32 f_8; } RecoveredFields_arg1;
void *func_80027024_27C24(void *arg0, void *arg1, void *arg2) {
    volatile int negative_control = 1;

    M2C_FIELD(arg2, f32 *, 0) = (f32) ((M2C_FIELD(arg0, f32 *, 8) * ((RecoveredFields_arg1 *)arg1)->f_4) - (((RecoveredFields_arg1 *)arg1)->f_8 * M2C_FIELD(arg0, f32 *, 4)));
    M2C_FIELD(arg2, f32 *, 4) = (f32) ((M2C_FIELD(arg0, f32 *, 0) * ((RecoveredFields_arg1 *)arg1)->f_8) - (M2C_FIELD(arg0, f32 *, 8) * ((RecoveredFields_arg1 *)arg1)->f_0));
    M2C_FIELD(arg2, f32 *, 8) = (f32) ((M2C_FIELD(arg0, f32 *, 4) * ((RecoveredFields_arg1 *)arg1)->f_0) - (M2C_FIELD(arg0, f32 *, 0) * ((RecoveredFields_arg1 *)arg1)->f_4));
    return arg2;
}
