typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void * func_801E1B30_60CF10(void *, f32, s32, f32, f32, f32, f32, f32);
void func_801CEE80_5FA260(s32);
s32 func_801D3A68_5FEE48(s32);
s32 func_801D365C_5FEA3C(void *);
u8 func_801D3854_5FEC34(void *);
void func_8000F3D8_FFD8(s32, s32, void *, f32);
s32 func_801D36CC_5FEAAC(void *);                   /* extern */
M2C_UNK func_801D7438_602818(M2C_UNK, s32, f32, f32); /* extern */
extern s32 D_8020EED0_63A2B0;

void func_80203AE4_62EEC4(void *arg0) {
    void *temp_s0;

    temp_s0 = M2C_FIELD(arg0, void **, 0x18);
    if ((func_801D365C_5FEA3C(arg0) != 0) || (func_801D36CC_5FEAAC(arg0) != 0)) {
        if (func_801D3854_5FEC34(arg0) >= 0x3C) {
            func_801D3A68_5FEE48(0xA);
            func_801D7438_602818(0xA, M2C_FIELD(temp_s0, s32 *, 8), M2C_FIELD(temp_s0, f32 *, 0xC), M2C_FIELD(temp_s0, f32 *, 0x10));
        }
        func_8000F3D8_FFD8(0x106, D_8020EED0_63A2B0 + 0xA0, temp_s0, 1500.0f);
        func_801CEE80_5FA260(4);
        func_801E1B30_60CF10(arg0, M2C_FIELD(temp_s0, f32 *, 0x1C) * 3.0f, M2C_FIELD(temp_s0, s32 *, 8), M2C_FIELD(temp_s0, f32 *, 0xC), M2C_FIELD(temp_s0, f32 *, 0x10), 0.0f, 0.0f, 0.0f);
    }
}
