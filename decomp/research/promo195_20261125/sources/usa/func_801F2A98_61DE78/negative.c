typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_8003521C_35E1C(s32);
s32 func_801D3B18_5FEEF8(void *, f32, u16);
void func_801D3F00_5FF2E0(void *, u16, s32);
void func_801D6508_6018E8(void *, f32);
extern M2C_UNK func_801F2B1C_61DEFC;

void func_801F2A98_61DE78(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    func_801D3B18_5FEEF8(arg0, M2C_FIELD(arg1, f32 *, 0x20) * 300.0f, 0x10U);
    func_801D3F00_5FF2E0(arg0, 0U, 8);
    func_801D6508_6018E8(arg0, -0.3f);
    if (M2C_FIELD(arg0, f32 *, 0x74) <= 0.0f) {
        func_8003521C_35E1C((s32) &func_801F2B1C_61DEFC);
    }
}
