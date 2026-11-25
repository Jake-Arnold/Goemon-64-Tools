typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
typedef struct { u8 pad_0[93]; u8 f_5D; u8 pad_5E[2]; f32 f_60; } RecoveredFields_arg0;
f32 func_8001B5AC_1C1AC(void *);                    /* extern */

void func_80217D0C_6816EC(void *arg0, void *arg1) {
    f32 temp_f2;

    M2C_FIELD(arg1, f32 *, 0x28) = (f32) (M2C_FIELD(arg1, f32 *, 0x28) + ((RecoveredFields_arg0 *)arg0)->f_60);
    temp_f2 = func_8001B5AC_1C1AC(arg1) - 1.0f;
    if (temp_f2 < M2C_FIELD(arg1, f32 *, 0x28)) {
        if (((RecoveredFields_arg0 *)arg0)->f_5D == 1) {
            M2C_FIELD(arg1, f32 *, 0x28) = 0.0f;
            return;
        }
        M2C_FIELD(arg1, f32 *, 0x28) = temp_f2;
    }
}
