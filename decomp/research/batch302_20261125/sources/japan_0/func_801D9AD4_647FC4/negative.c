typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
extern void (*D_801EE21C_65C70C[])();

void func_801D9AD4_647FC4(s8 *arg0) {
    volatile int negative_control = 1;

    D_801EE21C_65C70C[M2C_FIELD(arg0, u8 *, 0x9D)]();
    M2C_FIELD(arg0, f32 *, 0x64) = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0x64) + 28.0);
}
