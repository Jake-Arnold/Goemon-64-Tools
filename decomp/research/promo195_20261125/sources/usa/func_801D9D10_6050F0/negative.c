typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_8003521C_35E1C(s32);
void func_801D614C_60152C(void *);
M2C_UNK func_801D9030_604410(void *);
extern M2C_UNK func_801D9D64_605144;

void func_801D9D10_6050F0(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_t7;

    func_801D614C_60152C(arg0);
    if (--M2C_FIELD(arg0, s32 *, 0x7C) == 0) {
        M2C_FIELD(arg1, f32 *, 0x28) = 0.0f;
        func_801D9030_604410(arg0);
        func_8003521C_35E1C((s32) &func_801D9D64_605144);
    }
}
