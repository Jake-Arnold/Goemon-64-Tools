typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 func_801D2F40_5FE320(s32, M2C_UNK);             /* extern */
M2C_UNK func_801D5C30_601010(void *, s32, s32, s32, s32); /* extern */
s32 func_801D5D98_601178(void *, M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
u8 func_801D6C4C_60202C(s32, M2C_UNK);                   /* extern */
M2C_UNK func_801E599C_610D7C(void *);               /* extern */
M2C_UNK func_801EEE54_61A234(void *);               /* extern */
M2C_UNK func_801EEEA0_61A280(void *);               /* extern */

void func_801E5F64_611344(void *arg0, s32 arg1) {
    u8 sp2F;

    sp2F = func_801D6C4C_60202C(arg0, 0x3E4CCCCD);
    func_801EEE54_61A234(arg0);
    func_801EEEA0_61A280(arg0);
    func_801D5C30_601010(arg0, M2C_FIELD(arg0, s32 *, 0x70), M2C_FIELD(arg0, s32 *, 0x78), func_801D5D98_601178(arg0, 0x30, 0x41200000, 0x41000000) & 0xFFFF, 0);
    if ((func_801D2F40_5FE320(arg1, 0xC1A00000) == 0.0f) && (sp2F != 0)) {
        if (M2C_FIELD(arg0, s32 *, 0xEC) >= 2) {
            M2C_FIELD(arg0, s32 *, 0xEC) = 0;
            M2C_FIELD(arg0, s32 *, 0xD4) = 0;
        }
        func_801E599C_610D7C(arg0);
    }
}
