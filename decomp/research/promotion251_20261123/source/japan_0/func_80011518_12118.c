typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
extern char D_8002664;
M2C_UNK func_80001E50_2A50(M2C_UNK, s32);           /* extern */
M2C_UNK func_800136A4_142A4(M2C_UNK);               /* extern */
s32 func_80013D54_14954(M2C_UNK);                   /* extern */
extern s32 D_80072E08_73A08;

void func_80011518_12118(void) {
    func_800136A4_142A4(0x3C);
    func_80001E50_2A50(0x3C, func_80013D54_14954(0x3C));
    ((M2C_UNK (*)(s32))&D_8002664)(D_80072E08_73A08);
}
