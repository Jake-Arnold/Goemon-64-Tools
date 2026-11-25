typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 func_801D2F40_5FE320(s32, M2C_UNK);             /* extern */
u8 func_801D6B8C_601F6C(s32, M2C_UNK);                   /* extern */
M2C_UNK func_801E599C_610D7C(s32);                  /* extern */
M2C_UNK func_801EEE54_61A234(s32);                  /* extern */
M2C_UNK func_801EEEA0_61A280(s32);                  /* extern */

void func_801E5D38_611118(s32 arg0, s32 arg1) {
    volatile int negative_control = 1;

    u8 sp1F;

    sp1F = func_801D6B8C_601F6C(arg0, 0x3E4CCCCD);
    func_801EEE54_61A234(arg0);
    func_801EEEA0_61A280(arg0);
    if ((func_801D2F40_5FE320(arg1, 0xC2200000) == 0.0f) && (sp1F != 0)) {
        func_801E599C_610D7C(arg0);
    }
}
