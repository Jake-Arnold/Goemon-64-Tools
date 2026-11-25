typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801D34D0_5FE8B0(void *, M2C_UNK *, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801D3B18_5FEEF8(void *, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801D3F00_5FF2E0(void *, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801D606C_60144C();                     /* extern */
M2C_UNK func_801EEEC0_61A2A0(void *);               /* extern */
extern M2C_UNK D_8020B094_636474;
extern f64 D_8020DFC8_6393A8;
extern M2C_UNK func_801E628C_61166C;

void func_801E61A8_611588(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, f32 *, 0x10) >= -500.0f) {
        M2C_FIELD(arg0, f32 *, 0x78) = -8.0f;
        func_801D606C_60144C();
    }
    M2C_FIELD(arg1, f32 *, 0x28) = (f32) ((f64) M2C_FIELD(arg1, f32 *, 0x28) + D_8020DFC8_6393A8);
    if (M2C_FIELD(arg1, f32 *, 0x28) >= 10.0f) {
        M2C_FIELD(arg1, f32 *, 0x28) = 10.0f;
        func_801D34D0_5FE8B0(arg1, &D_8020B094_636474, 0, 0);
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x41;
        func_8003521C_35E1C(&func_801E628C_61166C);
    }
    func_801D3B18_5FEEF8(arg0, 0x42A00000, 8);
    func_801D3F00_5FF2E0(arg0, 0, 8);
    func_801EEEC0_61A2A0(arg0);
}
