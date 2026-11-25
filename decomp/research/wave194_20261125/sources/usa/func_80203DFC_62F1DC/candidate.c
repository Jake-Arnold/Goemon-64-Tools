typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
M2C_UNK func_8000F3D8_FFD8(M2C_UNK, s8 *, s8 *, M2C_UNK); /* extern */
M2C_UNK func_80035020_35C20();                      /* extern */
M2C_UNK func_801CEE80_5FA260(M2C_UNK);              /* extern */
s32 func_801D365C_5FEA3C(s32);                      /* extern */
s32 func_801D36CC_5FEAAC(s32);                      /* extern */
s32 func_801D3854_5FEC34(s32);                      /* extern */
M2C_UNK func_801D3A68_5FEE48(M2C_UNK);              /* extern */
M2C_UNK func_801D614C_60152C();                     /* extern */
M2C_UNK func_801D7438_602818(M2C_UNK, s32, s32, f32); /* extern */
M2C_UNK func_801E1B30_60CF10(s32, f32, s32, s32, f32, f32, f32, f32); /* extern */
extern s8 *D_8020EED0_63A2B0;

void func_80203DFC_62F1DC(s32 arg0, s8 *arg1) {
    s64 recovered_unused;
    s8 *sp34;

    sp34 = D_8020EED0_63A2B0 + 0x140;
    func_801D614C_60152C();
    if (M2C_FIELD(arg1, f32 *, 0x10) > 0.0f) {
        func_80035020_35C20();
        return;
    }
    if ((func_801D365C_5FEA3C(arg0) != 0) || (func_801D36CC_5FEAAC(arg0) != 0)) {
        if (func_801D3854_5FEC34(arg0) >= 0x3C) {
            func_801D3A68_5FEE48(5);
            func_801D7438_602818(5, M2C_FIELD(arg1, s32 *, 8), M2C_FIELD(arg1, s32 *, 0xC), M2C_FIELD(arg1, f32 *, 0x10));
        }
        if (func_801D365C_5FEA3C(arg0) == M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x1CC)) {
            if ((M2C_FIELD(sp34, u8 *, 0xE) == 0) && (M2C_FIELD(D_8020EED0_63A2B0, u8 *, 0x2C5) == 0)) {
                func_8000F3D8_FFD8(0x106, D_8020EED0_63A2B0 + 0xA0, arg1, 0x44BB8000);
            }
        } else {
            func_8000F3D8_FFD8(0x106, D_8020EED0_63A2B0 + 0xA0, arg1, 0x44BB8000);
        }
        func_801CEE80_5FA260(4);
        func_801E1B30_60CF10(arg0, M2C_FIELD(arg1, f32 *, 0x1C) * 3.0f, M2C_FIELD(arg1, s32 *, 8), M2C_FIELD(arg1, s32 *, 0xC), M2C_FIELD(arg1, f32 *, 0x10), 0.0f, 0.0f, 0.0f);
    }
}
