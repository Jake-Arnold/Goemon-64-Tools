typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
typedef struct { u8 pad_0[108]; f32 f_6C; f32 f_70; f32 f_74; f32 f_78; f32 f_7C; f32 f_80; } RecoveredFields_arg0;
s32 func_8001CF24_1DB24(void *);
void func_801F6F40_5B2F10(void *arg0, void *arg1, f32 arg2) {
    volatile int negative_control = 1;

    f32 sp2C;
    f32 sp28;
    f32 sp24;
    f32 temp_f12;
    f32 temp_f2;
    f32 var_f0;

    ((RecoveredFields_arg0 *)arg0)->f_6C = (f32) (((RecoveredFields_arg0 *)arg0)->f_6C + ((RecoveredFields_arg0 *)arg0)->f_78);
    var_f0 = ((RecoveredFields_arg0 *)arg0)->f_6C;
    ((RecoveredFields_arg0 *)arg0)->f_70 = (f32) (((RecoveredFields_arg0 *)arg0)->f_70 + ((RecoveredFields_arg0 *)arg0)->f_7C);
    temp_f2 = ((RecoveredFields_arg0 *)arg0)->f_70;
    ((RecoveredFields_arg0 *)arg0)->f_74 = (f32) (((RecoveredFields_arg0 *)arg0)->f_74 + ((RecoveredFields_arg0 *)arg0)->f_80);
    temp_f12 = ((RecoveredFields_arg0 *)arg0)->f_74;
    if ((arg2 * arg2) <= ((temp_f12 * temp_f12) + ((var_f0 * var_f0) + (temp_f2 * temp_f2)))) {
        sp24 = var_f0;
        sp28 = ((RecoveredFields_arg0 *)arg0)->f_70;
        sp2C = ((RecoveredFields_arg0 *)arg0)->f_74;
        func_8001CF24_1DB24(&sp24);
        ((RecoveredFields_arg0 *)arg0)->f_6C = (f32) (sp24 * arg2);
        var_f0 = ((RecoveredFields_arg0 *)arg0)->f_6C;
        ((RecoveredFields_arg0 *)arg0)->f_70 = (f32) (sp28 * arg2);
        ((RecoveredFields_arg0 *)arg0)->f_74 = (f32) (sp2C * arg2);
    }
    M2C_FIELD(arg1, f32 *, 8) = (f32) (M2C_FIELD(arg1, f32 *, 8) + var_f0);
    M2C_FIELD(arg1, f32 *, 0xC) = (f32) (M2C_FIELD(arg1, f32 *, 0xC) + ((RecoveredFields_arg0 *)arg0)->f_70);
    M2C_FIELD(arg1, f32 *, 0x10) = (f32) (M2C_FIELD(arg1, f32 *, 0x10) + ((RecoveredFields_arg0 *)arg0)->f_74);
}
