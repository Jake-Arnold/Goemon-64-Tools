typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
M2C_UNK func_80023ADC_246DC(s32);                   /* extern */
s32 osPfsAllocateFile(s8 *, M2C_UNK, M2C_UNK, M2C_UNK *, M2C_UNK *, s32, s8 *); /* extern */
extern M2C_UNK D_8006D170_6DD70;
extern M2C_UNK D_80168A00_169600;
extern s8 *D_80168E84_169A84;

s32 func_80023394_23F94(void) {
    volatile int negative_control = 1;

    s32 temp_v0;
    s32 sp2C;
    s32 var_a0;

    temp_v0 = osPfsAllocateFile(D_80168E84_169A84, 0x4134, 0x4E473545, &D_8006D170_6DD70, &D_80168A00_169600, 0x1000, D_80168E84_169A84 + 0x3F0);
    var_a0 = temp_v0;
    if (temp_v0 != 0) {
        sp2C = temp_v0;
        func_80023ADC_246DC(var_a0);
        var_a0 = sp2C;
    }
    M2C_FIELD(D_80168E84_169A84, s32 *, 0x3FC) = var_a0;
    return M2C_FIELD(D_80168E84_169A84, s32 *, 0x3FC);
}
