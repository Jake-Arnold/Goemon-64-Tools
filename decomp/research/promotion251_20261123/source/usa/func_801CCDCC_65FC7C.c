typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_801CCCE8_65FB98();                     /* static */
extern s32 D_801E9914_67C7C4;
extern s32 D_801E9930_67C7E0;

void func_801CCDCC_65FC7C(void) {
    func_801CCCE8_65FB98();
    if (D_801E9930_67C7E0 & 0x800) {
        D_801E9914_67C7C4 = 0;
    }
    if (D_801E9930_67C7E0 & 0x400) {
        D_801E9914_67C7C4 = 1;
    }
}
