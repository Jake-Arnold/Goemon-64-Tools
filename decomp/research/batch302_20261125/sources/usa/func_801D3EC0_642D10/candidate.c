typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
M2C_UNK func_800352EC_35EEC(M2C_UNK *);             /* extern */
s32 func_801CD504_63C354(s8 *);                   /* extern */
M2C_UNK func_801CD634_63C484(s8 *);               /* extern */
M2C_UNK func_801CD780_63C5D0(f32, s8 *);          /* extern */
M2C_UNK func_801CD834_63C684(s32, M2C_UNK *, M2C_UNK, M2C_UNK, s32); /* extern */
M2C_UNK func_801D2B90_6419E0(s8 *);               /* extern */
extern M2C_UNK D_801E8AD0_657920;
extern void (*D_801E8AD8_657928[])();
extern M2C_UNK func_801D47B0_643600;

void func_801D3EC0_642D10(s8 *arg0, s32 arg1) {
    u8 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u8 *, 0x9C);
    if ((temp_v0 != 0) && (M2C_FIELD(arg0, s8 *, 0x74) < 0)) {
        M2C_FIELD(arg0, u8 *, 0x9C) = 0U;
        M2C_FIELD(arg0, s8 *, 0x9D) = 0;
        func_800352EC_35EEC(&func_801D47B0_643600);
        return;
    }
    D_801E8AD8_657928[temp_v0](arg0, arg1);
    if (M2C_FIELD(arg0, u8 *, 0x9C) != 0) {
        if (func_801CD504_63C354(arg0) != 0) {
            func_801D2B90_6419E0(arg0);
            return;
        }
        func_801CD834_63C684(arg1, &D_801E8AD0_657920, 0, 0, 8);
        func_801CD634_63C484(arg0);
        func_801CD780_63C5D0(M2C_FIELD(arg0, f32 *, 0x64), arg0);
    }
}
