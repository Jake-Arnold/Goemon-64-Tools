typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_80037C20_38820(M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_80037C9C_3889C(M2C_UNK, M2C_UNK);      /* extern */
M2C_UNK func_80038BC8_397C8(M2C_UNK);               /* extern */
void *func_801E0950_60BD30(M2C_UNK, s32, M2C_UNK, f32); /* extern */
M2C_UNK func_801EE658_619A38();                     /* extern */
extern void *D_8020EED0_63A2B0;
extern M2C_UNK func_80208FB4_634394;

void func_80208EF4_6342D4(void *arg0, M2C_UNK arg1) {
    void *sp1C;

    sp1C = M2C_FIELD(M2C_FIELD(D_8020EED0_63A2B0, void **, 0x1D8), void **, 0x18);
    func_801EE658_619A38();
    if (M2C_FIELD(D_8020EED0_63A2B0, u8 *, 0x2C1) == 3) {
        func_80038BC8_397C8(0x10A);
        func_80037C9C_3889C(0, 0x64);
        func_80037C20_38820(0, 1, -1);
        M2C_FIELD(arg0, s32 *, 0x90) = (s32) M2C_FIELD(func_801E0950_60BD30(3, M2C_FIELD(sp1C, s32 *, 8), 0xC1200000, M2C_FIELD(sp1C, f32 *, 0x10) + 20.0f), s32 *, 0x18);
        M2C_FIELD(arg0, f32 *, 0x94) = 0.0f;
        func_8003521C_35E1C(&func_80208FB4_634394);
    }
}
