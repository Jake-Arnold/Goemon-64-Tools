typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_8003521C_35E1C(s32);
f32 func_801D2F40_5FE320(void *, f32);
u8 func_801D6B8C_601F6C(s32, M2C_UNK);
extern void *D_8020EED0_63A2B0;
extern M2C_UNK func_801FBB74_626F54;

void func_801FBAD8_626EB8(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_t7;

    func_801D2F40_5FE320(arg1, 100.0f);
    if (--M2C_FIELD(arg0, s32 *, 0x7C) == 0) {
        M2C_FIELD(D_8020EED0_63A2B0, s8 *, 0x2C1) = 3;
        func_8003521C_35E1C((s32) &func_801FBB74_626F54);
        return;
    }
    func_801D6B8C_601F6C((s32) arg0, 0x3E4CCCCD);
    M2C_FIELD(arg1, f32 *, 0x10) = (f32) ((f64) M2C_FIELD(arg1, f32 *, 0x10) - 0.5);
}
