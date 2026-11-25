typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801D31F0_5FE5D0(s32, M2C_UNK);              /* extern */
u8 func_801D3B18_5FEEF8(void *, M2C_UNK, M2C_UNK);  /* extern */
s32 func_801D3F00_5FF2E0(void *, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801D60E4_6014C4(void *);               /* extern */
M2C_UNK func_801EEEC0_61A2A0(void *);               /* extern */
extern f64 D_8020DF18_6392F8;
extern f64 D_8020DF20_639300;
extern M2C_UNK func_801E5144_610524;

void func_801E5064_610444(void *arg0, void *arg1) {
    u8 sp27;
    f64 temp_f0;

    func_801D31F0_5FE5D0(arg0, 0x42700000);
    sp27 = func_801D3B18_5FEEF8(arg0, 0x42A00000, 0xA);
    sp27 += func_801D3F00_5FF2E0(arg0, 0, 0xA);
    func_801D60E4_6014C4(arg0);
    func_801EEEC0_61A2A0(arg0);
    temp_f0 = (f64) M2C_FIELD(arg1, f32 *, 0x10);
    if ((temp_f0 < D_8020DF18_6392F8) && (D_8020DF20_639300 < temp_f0)) {
        M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x74) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
        if (sp27 == 2) {
            M2C_FIELD(arg0, s32 *, 0x7C) = 0x64;
            func_8003521C_35E1C(&func_801E5144_610524);
        }
    }
}
