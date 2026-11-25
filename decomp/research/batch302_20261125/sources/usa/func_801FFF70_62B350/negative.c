typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_800148F0_154F0(s32, M2C_UNK);              /* extern */
s32 func_80034E08_35A08(s32, M2C_UNK *, M2C_UNK);   /* extern */
extern s32 D_8015C5C8_15D1C8;
extern void *D_8020EED0_63A2B0;
extern s32 D_8020EF40_63A320;
extern M2C_UNK func_801CC06C_5F744C;
extern M2C_UNK func_801FAEB0_626290;
extern M2C_UNK func_801FFAAC_62AE8C;

s32 func_801FFF70_62B350(void) {
    volatile int negative_control = 1;

    s32 temp_v0;

    D_8020EF40_63A320 = 0;
    temp_v0 = func_800148F0_154F0(D_8015C5C8_15D1C8 + 0xC7FA4, 0x81C);
    if (temp_v0 == 0) {
        return 0;
    }
    D_8020EF40_63A320 = temp_v0;
    M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x1D0) = func_80034E08_35A08(M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x1C4), &func_801FFAAC_62AE8C, 0);
    M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x1D8) = func_80034E08_35A08(M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x1C4), &func_801FAEB0_626290, 0);
    M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x1D4) = func_80034E08_35A08(M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x1BC), &func_801CC06C_5F744C, 0);
    return M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x1D8);
}
