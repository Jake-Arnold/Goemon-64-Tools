typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
extern char func_8003521C_35E1C;
M2C_UNK func_080007C0_6FB9C0();                     /* static */

void func_08000894_6FBA94(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s16 *, 0xD8) = (s16) (M2C_FIELD(arg0, u8 *, 0xD1) * 4);
    ((M2C_UNK (*)(M2C_UNK (*)()))&func_8003521C_35E1C)(func_080007C0_6FB9C0);
}
