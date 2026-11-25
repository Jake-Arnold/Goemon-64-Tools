typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80034E8C_35A8C(s32);
f32 func_801D8660_6030E0(void *, f32);
void func_801D8DE4_603864(void *);
extern M2C_UNK func_801F9B6C_6245EC;

void func_801F9B00_624580(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (func_801D8660_6030E0(arg1, 50.0f) == 0.0f) {
        M2C_FIELD(arg0, u8 *, 0x30) = (u8) (M2C_FIELD(arg0, u8 *, 0x30) | 2);
        func_801D8DE4_603864(arg0);
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x1E;
        func_80034E8C_35A8C((s32) &func_801F9B6C_6245EC);
    }
}
