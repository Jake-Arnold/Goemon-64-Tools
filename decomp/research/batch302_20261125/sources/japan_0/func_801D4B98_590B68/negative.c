typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
s32 func_8001CCDC_1D8DC(s8 *, M2C_UNK, f32, f32, f32);
void func_801D4B98_590B68(s8 *arg0, f32 arg1, f32 arg2, f32 arg3) {
    volatile int negative_control = 1;

    func_8001CCDC_1D8DC(M2C_FIELD(arg0, s8 **, 0x18), (s32) (arg0 + 0x84), arg1, arg2, arg3);
}
