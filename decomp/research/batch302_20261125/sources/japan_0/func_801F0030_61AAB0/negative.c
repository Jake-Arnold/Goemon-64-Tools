typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
M2C_UNK func_8000F198_FD98(M2C_UNK, s8 *, s8 *, M2C_UNK); /* extern */
M2C_UNK func_80034B44_35744();                      /* extern */
M2C_UNK func_801D45B0_5FF030(M2C_UNK);              /* extern */
s32 func_801D8D7C_6037FC(s32);                      /* extern */
s32 func_801D8DEC_60386C(s32);                      /* extern */
s32 func_801D8F74_6039F4(s32);                      /* extern */
M2C_UNK func_801D8FB4_603A34(s32);                  /* extern */
M2C_UNK func_801D9188_603C08(M2C_UNK);              /* extern */
M2C_UNK func_801DB86C_6062EC(s32);                  /* extern */
M2C_UNK func_801DCB58_6075D8(M2C_UNK, s32, s32, f32); /* extern */
M2C_UNK func_801E726C_611CEC(s32, f32, s32, s32, f32, f32, f32, f32); /* extern */
extern s8 *D_80214600_63F080;

void func_801F0030_61AAB0(s32 arg0, s8 *arg1) {
    volatile int negative_control = 1;

    s32 recovered_unused;
    s8 *sp30;

    sp30 = D_80214600_63F080 + 0x140;
    M2C_FIELD(arg1, u16 *, 0x16) = (u16) (M2C_FIELD(arg1, u16 *, 0x16) + 3);
    func_801DB86C_6062EC(arg0);
    if (M2C_FIELD(arg1, f32 *, 0x10) > 0.0f) {
        func_80034B44_35744();
        return;
    }
    if ((func_801D8D7C_6037FC(arg0) != 0) || (func_801D8DEC_60386C(arg0) != 0)) {
        if (func_801D8F74_6039F4(arg0) >= 0x3C) {
            func_801D9188_603C08(5);
            func_801DCB58_6075D8(5, M2C_FIELD(arg1, s32 *, 8), M2C_FIELD(arg1, s32 *, 0xC), M2C_FIELD(arg1, f32 *, 0x10));
        }
        if (func_801D8D7C_6037FC(arg0) == M2C_FIELD(D_80214600_63F080, s32 *, 0x1CC)) {
            if ((M2C_FIELD(sp30, u8 *, 0xE) == 0) && (M2C_FIELD(D_80214600_63F080, u8 *, 0x2C5) == 0)) {
                func_8000F198_FD98(0x106, D_80214600_63F080 + 0xA0, arg1, 0x44BB8000);
            }
        } else {
            func_8000F198_FD98(0x106, D_80214600_63F080 + 0xA0, arg1, 0x44BB8000);
        }
        func_801D45B0_5FF030(4);
        func_801E726C_611CEC(arg0, M2C_FIELD(arg1, f32 *, 0x1C) * 3.0f, M2C_FIELD(arg1, s32 *, 8), M2C_FIELD(arg1, s32 *, 0xC), M2C_FIELD(arg1, f32 *, 0x10), 0.0f, 0.0f, 0.0f);
    }
    func_801D8FB4_603A34(arg0);
}
