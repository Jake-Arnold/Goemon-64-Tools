typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_8003521C_35E1C(s32);
s32 func_801D4D0C_6000EC(f32, f32, f32, f32);
void func_801E4194_60F574(s32, s32, s32, s32);
extern void *D_8020EED0_63A2B0;
extern M2C_UNK func_80207C8C_63306C;

void func_80207C08_632FE8(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if ((M2C_FIELD(D_8020EED0_63A2B0, u8 *, 0x2C1) == 2) && (func_801D4D0C_6000EC(1.0f, 0.0f, 0.0f, 0.0f) != 0)) {
        func_801E4194_60F574(0xFF, 0xFF, 0xFF, 0xFF);
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x64;
        func_8003521C_35E1C((s32) &func_80207C8C_63306C);
    }
}
