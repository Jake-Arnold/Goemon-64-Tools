typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
extern void *D_80214600_63F080;
extern void *func_80214670_5CFC00;

void func_80205C00_630680(void *arg0, M2C_UNK arg1) {
    s32 temp_t7;

    if (--M2C_FIELD(arg0, s32 *, 0x7C) == 0) {
        M2C_FIELD(func_80214670_5CFC00, s8 *, 5) = 1;
    }
    M2C_FIELD(D_80214600_63F080, s8 *, 0x2C1) = 2;
}
