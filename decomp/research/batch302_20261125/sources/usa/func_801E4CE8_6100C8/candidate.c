typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_80037C20_38820(M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_80037C9C_3889C(M2C_UNK, M2C_UNK);      /* extern */
M2C_UNK func_80038BC8_397C8(M2C_UNK);               /* extern */
f32 func_801D2F40_5FE320(void *, M2C_UNK);          /* extern */
M2C_UNK func_801D31CC_5FE5AC(void *, M2C_UNK *);    /* extern */
M2C_UNK func_801E0950_60BD30(M2C_UNK, s32, f32, s32); /* extern */
M2C_UNK func_801E1084_60C464(void *, s32, f32, s32); /* extern */
extern M2C_UNK D_8020B1D0_6365B0;
extern f64 D_8020DF10_6392F0;
extern M2C_UNK func_801E4DF8_6101D8;

void func_801E4CE8_6100C8(void *arg0, void *arg1) {
    if (func_801D2F40_5FE320(arg1, 0xC3960000) == 0.0f) {
        func_801D31CC_5FE5AC(arg0, &D_8020B1D0_6365B0);
        func_80038BC8_397C8(0x4A);
        func_801E1084_60C464(arg0, M2C_FIELD(arg1, s32 *, 8), M2C_FIELD(arg1, f32 *, 0xC) + 50.0f, M2C_FIELD(arg1, s32 *, 0x10));
        func_801E0950_60BD30(1, M2C_FIELD(arg1, s32 *, 8), M2C_FIELD(arg1, f32 *, 0xC), M2C_FIELD(arg1, s32 *, 0x10));
        func_80037C9C_3889C(0, 0x78);
        func_80037C20_38820(0, 1, 0xAAAAAAAA);
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x78;
        M2C_FIELD(arg0, s32 *, 0x80) = 0;
        func_8003521C_35E1C(&func_801E4DF8_6101D8);
    }
    if (M2C_FIELD(arg1, f32 *, 0x28) > 13.0f) {
        M2C_FIELD(arg1, f32 *, 0xC) = (f32) ((f64) M2C_FIELD(arg1, f32 *, 0xC) + D_8020DF10_6392F0);
    }
}
