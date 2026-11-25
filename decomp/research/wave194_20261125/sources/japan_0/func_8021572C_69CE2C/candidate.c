typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
typedef struct { u8 pad_0[24]; void * f_18; u8 pad_1C[64]; f32 f_5C; f32 f_60; f32 f_64; f32 f_68; f32 f_6C; f32 f_70; } RecoveredFields_arg0;
void func_8021572C_69CE2C(void *arg0, M2C_UNK arg1) {
    void *temp_v0;

    ((RecoveredFields_arg0 *)arg0)->f_5C = (f32) (((RecoveredFields_arg0 *)arg0)->f_5C + ((RecoveredFields_arg0 *)arg0)->f_68);
    temp_v0 = ((RecoveredFields_arg0 *)arg0)->f_18;
    ((RecoveredFields_arg0 *)arg0)->f_60 = (f32) (((RecoveredFields_arg0 *)arg0)->f_60 + ((RecoveredFields_arg0 *)arg0)->f_6C);
    ((RecoveredFields_arg0 *)arg0)->f_64 = (f32) (((RecoveredFields_arg0 *)arg0)->f_64 + ((RecoveredFields_arg0 *)arg0)->f_70);
    M2C_FIELD(temp_v0, f32 *, 8) = (f32) ((RecoveredFields_arg0 *)arg0)->f_5C;
    M2C_FIELD(temp_v0, f32 *, 0xC) = (f32) ((RecoveredFields_arg0 *)arg0)->f_60;
    M2C_FIELD(temp_v0, f32 *, 0x10) = (f32) ((RecoveredFields_arg0 *)arg0)->f_64;
}
