typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80034F5C_35B5C(s32);
void func_801EDAA8_65BF98(void *, s8, f32, f32, f32, f32, f32, f32, f32, f32, f32);
extern M2C_UNK func_801D78EC_645DDC;

void func_801D7890_645D80(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s16 *, 0xAC) = 0;
    func_801EDAA8_65BF98(arg0, 0, 20.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f);
    func_80034F5C_35B5C((s32) &func_801D78EC_645DDC);
}
