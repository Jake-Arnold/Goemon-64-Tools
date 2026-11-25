typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
typedef struct { u8 pad_0[208]; u8 f_D0; u8 pad_D1[3]; u8 f_D4; u8 f_D5; } RecoveredFields_arg0;
void func_80034B44_35744(void);
void * func_8021EFDC_5DA56C(void *, s32, s32, s32, s32);
void func_80218834_5D3DC4(void *arg0, M2C_UNK arg1) {
    volatile int negative_control = 1;

    u8 temp_t9;

    if (((RecoveredFields_arg0 *)arg0)->f_D4 == 0xFF) {
        ((RecoveredFields_arg0 *)arg0)->f_D5 = 0xFAU;
    }
    if (((RecoveredFields_arg0 *)arg0)->f_D4 == 0) {
        ((RecoveredFields_arg0 *)arg0)->f_D5 = 5U;
    }
    temp_t9 = ((RecoveredFields_arg0 *)arg0)->f_D4 + ((RecoveredFields_arg0 *)arg0)->f_D5;
    ((RecoveredFields_arg0 *)arg0)->f_D4 = temp_t9;
    func_8021EFDC_5DA56C(arg0, 0x8C, temp_t9 & 0xFF, 0xFF, 0x50);
    if (((RecoveredFields_arg0 *)arg0)->f_D0 != 0) {
        func_80034B44_35744();
    }
}
