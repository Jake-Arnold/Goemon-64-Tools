typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8000F3D8_FFD8(M2C_UNK, s32, void *, M2C_UNK);
M2C_UNK func_80035020_35C20();
M2C_UNK func_801CEE80_5FA260(M2C_UNK);
s32 func_801D365C_5FEA3C(void *);
s32 func_801D36CC_5FEAAC(void *);
s32 func_801D3854_5FEC34(void *);
M2C_UNK func_801D3894_5FEC74(void *);
M2C_UNK func_801D3A68_5FEE48(M2C_UNK);
M2C_UNK func_801D614C_60152C();
M2C_UNK func_801D7438_602818(M2C_UNK, s32, s32, f32);
M2C_UNK func_801E1B30_60CF10(void *, f32, s32, s32, f32, f32, f32, f32);
extern s32 D_8020EED0_63A2B0;

void func_801F85C8_6239A8(void *arg0, void *arg1) {
    s32 temp_t7;

    func_801D614C_60152C();
    if (M2C_FIELD(arg0, f32 *, 0x78) < 0.0f) {

    if ((M2C_FIELD(arg0, s32 *, 0x7C) -= 1) < 0) {
            func_80035020_35C20();
            return;
        }
    }
    if (M2C_FIELD(arg1, f32 *, 0x10) > 0.0f) {
        func_80035020_35C20();
        return;
    }
    if ((func_801D365C_5FEA3C(arg0) != 0) || (func_801D36CC_5FEAAC(arg0) != 0)) {
        if (func_801D3854_5FEC34(arg0) >= 0x3C) {
            func_801D3A68_5FEE48(5);
            func_801D7438_602818(5, M2C_FIELD(arg1, s32 *, 8), M2C_FIELD(arg1, s32 *, 0xC), M2C_FIELD(arg1, f32 *, 0x10));
        }
        func_8000F3D8_FFD8(0x106, D_8020EED0_63A2B0 + 0xA0, arg1, 0x44BB8000);
        func_801CEE80_5FA260(4);
        func_801E1B30_60CF10(arg0, M2C_FIELD(arg1, f32 *, 0x1C) * 3.0f, M2C_FIELD(arg1, s32 *, 8), M2C_FIELD(arg1, s32 *, 0xC), M2C_FIELD(arg1, f32 *, 0x10), 0.0f, 0.0f, 0.0f);
    }
    func_801D3894_5FEC74(arg0);
}
