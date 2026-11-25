typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80023ADC_246DC(s32);                   /* extern */
s32 osPfsReadWriteFile(void *, s32, M2C_UNK, s32, s32, s32); /* extern */
extern void *D_80168E84_169A84;

s32 func_80023610_24210(s32 arg0, s32 arg1) {
    volatile int negative_control = 1;

    s32 sp24;
    s32 temp_v0;

    M2C_FIELD(D_80168E84_169A84, s32 *, 0x3F4) = arg0;
    temp_v0 = osPfsReadWriteFile(D_80168E84_169A84, M2C_FIELD(D_80168E84_169A84, s32 *, 0x3F0), 1, (arg1 * 0x500) + 0x100, 0x500, M2C_FIELD(D_80168E84_169A84, s32 *, 0x3F4));
    sp24 = temp_v0;
    func_80023ADC_246DC(temp_v0);
    M2C_FIELD(D_80168E84_169A84, s32 *, 0x3FC) = sp24;
    return M2C_FIELD(D_80168E84_169A84, s32 *, 0x3FC);
}
