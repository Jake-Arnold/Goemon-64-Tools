typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_801EDD04_5A9CD4(void *, s32);
s32 func_801F38F8_5AF8C8(void *arg0) {
    s32 sp34;
    s32 sp30;
    s32 sp2C;
    s32 sp28;
    s32 sp24;

    sp24 = func_801EDD04_5A9CD4(arg0, 0x1E);
    sp28 = func_801EDD04_5A9CD4(arg0, 0x1D);
    sp2C = func_801EDD04_5A9CD4(arg0, 0x19);
    sp30 = func_801EDD04_5A9CD4(arg0, 0x18);
    sp34 = func_801EDD04_5A9CD4(arg0, 0x17);
    return ((func_801EDD04_5A9CD4(arg0, 0x1F) + sp34 + sp30 + sp2C + sp28 + sp24) < 3) ^ 1;
}
