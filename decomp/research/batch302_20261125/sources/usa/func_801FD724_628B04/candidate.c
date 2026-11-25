typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
void func_801D36C4_5FEAA4(s8 *);
void func_80038BC8_397C8(s32);
void func_8000F240_FE40(s32, s32, s8 *);
s32 func_801D6330_601710(s8 *, f32);
s32 func_801D3118_5FE4F8(s8 *, f32, f32);
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
f32 func_801D31F0_5FE5D0(s8 *, M2C_UNK);          /* extern */
s32 func_801D365C_5FEA3C(s8 *);                   /* extern */
M2C_UNK func_801FFDFC_62B1DC();                     /* extern */
extern s8 *D_8020EED0_63A2B0;
extern M2C_UNK func_801FD840_628C20;

void func_801FD724_628B04(s8 *arg0, s8 *arg1) {
    s8 *sp24;

    sp24 = D_8020EED0_63A2B0 + 0x140;
    M2C_FIELD(arg0, f32 *, 0x74) = 12.0f;
    if (func_801D6330_601710(arg0, -40.0f) != 0) {
        if (func_801D3118_5FE4F8(arg1, 80.0f, 22.0f) != 0) {
            func_8000F240_FE40(0x247, (s32) (D_8020EED0_63A2B0 + 0xA0), arg1);
        }
        if (func_801D31F0_5FE5D0(arg0, 0x42A00000) == 0.0f) {
            M2C_FIELD(arg0, s8 *, 0x30) = 1;
            M2C_FIELD(arg0, s32 *, 0x48) = 0;
            M2C_FIELD(arg0, s8 *, 0x4C) = 0;
            func_801FFDFC_62B1DC();
            func_8003521C_35E1C(&func_801FD840_628C20);
            return;
        }
        goto block_5;
    }
block_5:
    if ((func_801D365C_5FEA3C(arg0) == M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x1CC)) && (M2C_FIELD(sp24, u8 *, 0xE) == 0) && (M2C_FIELD(D_8020EED0_63A2B0, u8 *, 0x2C5) == 0)) {
        M2C_FIELD(arg0, s8 *, 0x30) = 1;
        M2C_FIELD(arg0, s32 *, 0x48) = 0;
        M2C_FIELD(arg0, s8 *, 0x4C) = 0;
        func_80038BC8_397C8(0x24A);
    }
    func_801D36C4_5FEAA4(arg0);
}
