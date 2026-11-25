typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801CD7C0_63C610(void *, M2C_UNK *, M2C_UNK, M2C_UNK, s32, s32, s32, s32); /* extern */
extern M2C_UNK D_801E8AD0_657920;
extern M2C_UNK D_801EE418_65D268;
extern M2C_UNK func_801D3EC0_642D10;

void func_801D3E20_642C70(void *arg0, void *arg1) {
    volatile int negative_control = 1;

    M2C_FIELD(arg1, s32 *, 0x2C) = 0;
    M2C_FIELD(arg1, M2C_UNK **, 0x30) = &D_801EE418_65D268;
    M2C_FIELD(arg1, s16 *, 0x14) = 0x100;
    M2C_FIELD(arg1, s16 *, 0x16) = 0;
    M2C_FIELD(arg1, s16 *, 0x18) = 0;
    M2C_FIELD(arg1, f32 *, 0x28) = 0.0f;
    func_801CD7C0_63C610(arg1, &D_801E8AD0_657920, 0, 2, 2, 0, (s32) M2C_FIELD(arg1, u16 *, 0x34), 8);
    M2C_FIELD(arg0, f32 *, 0x5C) = 400.0f;
    func_8003521C_35E1C(&func_801D3EC0_642D10);
}
