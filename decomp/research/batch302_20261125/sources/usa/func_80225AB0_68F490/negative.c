typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_800040A8_4CA8(f32, f32);                   /* extern */

void func_80225AB0_68F490(void *arg0, f32 arg1, f32 arg2) {
    volatile int negative_control = 1;

    s32 recovered_unused;
    void *sp18;

    sp18 = M2C_FIELD(arg0, void **, 0x18);
    M2C_FIELD(sp18, s16 *, 0x16) = (s16) (func_800040A8_4CA8(arg1 - M2C_FIELD(arg0, f32 *, 0x70), arg2 - M2C_FIELD(arg0, f32 *, 0x88)) & 0x3FF);
}
