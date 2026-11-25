typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_800148F0_154F0(s32, M2C_UNK);              /* extern */
s32 func_80034DD8_359D8(M2C_UNK *, M2C_UNK);        /* extern */
M2C_UNK func_80038BC8_397C8(M2C_UNK);               /* extern */
extern s32 D_8015C5C8_15D1C8;
extern s32 D_8020EF10_63A2F0;
extern M2C_UNK func_801E41F0_60F5D0;

s32 func_801E45B4_60F994(void) {
    s32 sp18;
    s32 temp_v0;
    s32 temp_v0_2;

    D_8020EF10_63A2F0 = 0;
    temp_v0_2 = func_800148F0_154F0(D_8015C5C8_15D1C8 + 0xC7FA4, 4);
    if (temp_v0_2 == 0) {
        return 0;
    }
    D_8020EF10_63A2F0 = temp_v0_2;
    temp_v0 = func_80034DD8_359D8(&func_801E41F0_60F5D0, 0);
    sp18 = temp_v0;
    func_80038BC8_397C8(0x43);
    return temp_v0;
}
