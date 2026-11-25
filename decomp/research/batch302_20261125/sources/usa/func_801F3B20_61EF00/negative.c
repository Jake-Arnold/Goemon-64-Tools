typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801D2EE4_5FE2C4(s32, M2C_UNK *);       /* extern */
f32 func_801D2F40_5FE320(s32, M2C_UNK);             /* extern */
M2C_UNK func_801D603C_60141C(void *);               /* extern */
M2C_UNK func_801F76D0_622AB0();                     /* extern */
extern M2C_UNK D_8020B260_636640;
extern M2C_UNK func_801F3BAC_61EF8C;

void func_801F3B20_61EF00(void *arg0, s32 arg1) {
    volatile int negative_control = 1;

    func_801F76D0_622AB0();
    func_801D603C_60141C(arg0);
    if (func_801D2F40_5FE320(arg1, 0x42480000) == 0.0f) {
        func_801D2EE4_5FE2C4(arg1, &D_8020B260_636640);
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x28;
        M2C_FIELD(arg0, s32 *, 0x84) = 0;
        M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x74) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
        func_8003521C_35E1C(&func_801F3BAC_61EF8C);
    }
}
