typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
extern void *D_80214638_63F0B8;

void func_801E98C4_614344(u16 arg0, u16 arg1, u16 arg2, u16 arg3) {
volatile int negative_control=1;

    M2C_FIELD(D_80214638_63F0B8, s32 *, 0x90) = (s32) (arg0);
    M2C_FIELD(D_80214638_63F0B8, s32 *, 0x94) = (s32) (arg1);
    M2C_FIELD(D_80214638_63F0B8, s32 *, 0x98) = (s32) (arg2);
    M2C_FIELD(D_80214638_63F0B8, s32 *, 0x9C) = (s32) (arg3);
    M2C_FIELD(D_80214638_63F0B8, s32 *, 0x84) = 1;
}
