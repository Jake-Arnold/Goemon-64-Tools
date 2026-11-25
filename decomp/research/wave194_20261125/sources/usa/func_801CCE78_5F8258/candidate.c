typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80034EF8_35AF8(s32);                   /* extern */
M2C_UNK func_80034F20_35B20();                      /* extern */
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801D614C_60152C(void *);               /* extern */
extern s32 D_8015C5D8_15D1D8;
extern f32 D_8020CF80_638360;
extern void *D_8020EED0_63A2B0;
extern M2C_UNK func_801CC89C_5F7C7C;

void func_801CCE78_5F8258(s32 arg0, M2C_UNK arg1) {
    s32 temp_a0_2;
    void *sp20;
    void *temp_a0;
    void *temp_s0;

    temp_s0 = D_8020EED0_63A2B0;
    temp_a0 = M2C_FIELD(temp_s0, void **, 0x18);
    M2C_FIELD(temp_a0, f32 *, 0x70) = 0.0f;
    M2C_FIELD(temp_a0, f32 *, 0x74) = 0.0f;
    M2C_FIELD(temp_a0, f32 *, 0x78) = (f32) D_8020CF80_638360;
    func_801D614C_60152C(temp_a0);
    sp20 = M2C_FIELD(temp_s0, void **, 0x1C);
    temp_a0_2 = M2C_FIELD(temp_s0, s32 *, 0);
    if (temp_a0_2 != 0) {
        func_80034EF8_35AF8(temp_a0_2);
        if (D_8015C5D8_15D1D8 == 2) {
            func_80034EF8_35AF8(M2C_FIELD(temp_s0, s32 *, 0xC));
        }
        M2C_FIELD(temp_s0, s32 *, 0) = 0;
        M2C_FIELD(temp_s0, s32 *, 0xC) = 0;
    }
    if ((f64) M2C_FIELD(sp20, f32 *, 0x10) <= -8.0) {
        func_80034F20_35B20();
        func_8003521C_35E1C(&func_801CC89C_5F7C7C);
    }
}
