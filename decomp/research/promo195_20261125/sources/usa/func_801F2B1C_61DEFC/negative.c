typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_8003521C_35E1C(s32);
s32 func_801D3B18_5FEEF8(void *, f32, u16);
extern M2C_UNK func_801F2B7C_61DF5C;

void func_801F2B1C_61DEFC(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (func_801D3B18_5FEEF8(arg0, M2C_FIELD(arg1, f32 *, 0x20) * 300.0f, 0x10U) != 0) {
        M2C_FIELD(arg0, s32 *, 0x90) = 0;
        M2C_FIELD(arg0, s32 *, 0x7C) = 4;
        func_8003521C_35E1C((s32) &func_801F2B7C_61DF5C);
    }
}
