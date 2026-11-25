typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80038BC8_397C8(s32);
void func_801DF868_60AC48(s32, f32, f32, f32, f32);
f32 func_801D2F40_5FE320(void *, f32);
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801DFB90_60AF70(s32, M2C_UNK, M2C_UNK, M2C_UNK, f32, f32, f32, f32, f32, f32); /* extern */
extern void *D_8020EED0_63A2B0;
extern M2C_UNK func_801FA7D8_625BB8;

void func_801FA688_625A68(s32 arg0, void *arg1) {
    M2C_FIELD(arg1, f32 *, 0x10) = (f32) (M2C_FIELD(arg1, f32 *, 0x10) - 1.0f);
    if (M2C_FIELD(arg1, f32 *, 0x10) < -300.0f) {
        M2C_FIELD(arg1, f32 *, 0x10) = -300.0f;
    }
    if ((func_801D2F40_5FE320(arg1, 20.0f) == 0.0f) && (M2C_FIELD(arg1, f32 *, 0x10) <= -300.0f)) {
        func_80038BC8_397C8(0x245);
        func_801DF868_60AC48(arg0, M2C_FIELD(arg1, f32 *, 8), M2C_FIELD(arg1, f32 *, 0xC), -480.0f, 0.25f);
        M2C_FIELD(D_8020EED0_63A2B0, s8 *, 0x2C1) = 2;
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x28;
        func_8003521C_35E1C(&func_801FA7D8_625BB8);
    }
    M2C_FIELD(arg0, f32 *, 0x90) = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0x90) + 6.5);
    func_801DFB90_60AF70(arg0, 8, 0x3F800000, 0x3F4CCCCD, M2C_FIELD(arg1, f32 *, 8), M2C_FIELD(arg1, f32 *, 0xC), -M2C_FIELD(arg0, f32 *, 0x90), 20.0f, 20.0f, 20.0f);
}
