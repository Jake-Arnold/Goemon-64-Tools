typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
f32 func_801D3018_5FE3F8(s8 *, f32);
s32 func_8000E9F4_F5F4(f32, f32, s8 *);
s32 func_8000E630_F230(f32, u16, f32 *, f32 *);
s32 func_801D6330_601710(s8 *, f32);
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801FFDFC_62B1DC();                     /* extern */
extern s32 D_8020EED0_63A2B0;
extern M2C_UNK func_801FF380_62A760;

void func_801FF294_62A674(s8 *arg0, s8 *arg1) {
    s8 *sp24;

    sp24 = D_8020EED0_63A2B0 + 0x140;
    M2C_FIELD(arg0, f32 *, 0x74) = 6.0f;
    func_801D6330_601710(arg0, -100.0f);
    func_801D3018_5FE3F8(arg1, 45.0f);
    M2C_FIELD(arg0, f32 *, 0x90) = (f32) (M2C_FIELD(arg0, f32 *, 0x90) - 10.0f);
    func_8000E630_F230(M2C_FIELD(arg0, f32 *, 0x90), M2C_FIELD(arg0, u16 *, 0x96), arg1 + 8, arg1 + 0x10);
    M2C_FIELD(arg1, s16 *, 0x16) = func_8000E9F4_F5F4(0.0f, 0.0f, arg1);
    func_801D3018_5FE3F8(arg1, 60.0f);
    if (M2C_FIELD(sp24, s32 *, 0x34) == 0) {
        if (M2C_FIELD(arg0, s32 *, 0xE4) >= 2) {
            M2C_FIELD(arg0, s32 *, 0x7C) = 0x14;
        } else {
            M2C_FIELD(arg0, s32 *, 0x7C) = 0x28;
        }
        func_801FFDFC_62B1DC();
        func_8003521C_35E1C(&func_801FF380_62A760);
    }
}
