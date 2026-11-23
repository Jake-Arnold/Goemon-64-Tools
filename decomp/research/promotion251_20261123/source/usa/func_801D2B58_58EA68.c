typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_801D2C88_58EB98(s32, s32);             /* static */
M2C_UNK func_801D2D10_58EC20(s32, M2C_UNK);

void func_801D2B58_58EA68(s32 arg0, s32 arg1) {
    func_801D2D10_58EC20(arg0, 0x41A00000);
    func_801D2C88_58EB98(arg0, arg1);
}
