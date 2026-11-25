typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
s32 func_801D4408_5FF7E8(s32, s32);
void func_801D2EE4_5FE2C4(s8 *, s8 *);
s32 func_8000E39C_EF9C(f32, f32, f32, f32, s8 *);
void func_801F76D0_622AB0(s8 *);
f32 func_801D2F40_5FE320(s8 *, f32);
void func_801D6508_6018E8(s8 *, f32);
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
s32 func_801D3B18_5FEEF8(s8 *, f32, M2C_UNK);     /* extern */
M2C_UNK func_801D725C_60263C(s8 *, M2C_UNK);      /* extern */
extern M2C_UNK D_80085D8;
extern M2C_UNK D_8020B290_636670;
extern f64 D_8020E680_639A60;
extern M2C_UNK func_801F40DC_61F4BC;

void func_801F3FC0_61F3A0(s8 *arg0, s8 *arg1) {
    volatile int negative_control = 1;

    u8 sp2F;

    func_801F76D0_622AB0(arg0);
    func_801D6508_6018E8(arg0, -0.5f);
    func_801D725C_60263C(arg0 + 0x74, 0x40C00000);
    sp2F = func_801D4408_5FF7E8((s32) arg0, -0x3E600000);
    if ((func_801D2F40_5FE320(arg1, 30.0f) == 0.0f) && (func_801D3B18_5FEEF8(arg0, M2C_FIELD(arg1, f32 *, 0x20) * 300.0f, 0x10) != 0) && (sp2F != 0)) {
        func_801D2EE4_5FE2C4(arg1, &D_8020B290_636670);
        M2C_FIELD(arg0, s8 *, 0x30) = 1;
        M2C_FIELD(arg0, M2C_UNK **, 0x48) = &D_80085D8;
        M2C_FIELD(arg0, s8 *, 0x4C) = 0x51;
        func_8000E39C_EF9C(10.0f, 0.0f, (f32) ((f64) M2C_FIELD(arg1, f32 *, 0x20) * D_8020E680_639A60), 0.0f, arg0);
        func_8003521C_35E1C(&func_801F40DC_61F4BC);
    }
}
