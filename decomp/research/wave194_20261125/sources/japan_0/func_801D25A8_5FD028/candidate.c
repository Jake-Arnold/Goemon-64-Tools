typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80034B68_35768(s32);                   /* extern */
M2C_UNK func_80034B90_35790();                      /* extern */
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
M2C_UNK func_801DB86C_6062EC(void *);               /* extern */
extern s32 D_80161DC8_1629C8;
extern f32 D_802126B0_63D130;
extern void *D_80214600_63F080;
extern M2C_UNK func_801D1FCC_5FCA4C;

void func_801D25A8_5FD028(s32 arg0, M2C_UNK arg1) {
    s32 temp_a0_2;
    void *sp20;
    void *temp_a0;
    void *temp_s0;

    temp_s0 = D_80214600_63F080;
    temp_a0 = M2C_FIELD(temp_s0, void **, 0x18);
    M2C_FIELD(temp_a0, f32 *, 0x70) = 0.0f;
    M2C_FIELD(temp_a0, f32 *, 0x74) = 0.0f;
    M2C_FIELD(temp_a0, f32 *, 0x78) = (f32) D_802126B0_63D130;
    func_801DB86C_6062EC(temp_a0);
    sp20 = M2C_FIELD(temp_s0, void **, 0x1C);
    temp_a0_2 = M2C_FIELD(temp_s0, s32 *, 0);
    if (temp_a0_2 != 0) {
        func_80034B68_35768(temp_a0_2);
        if (D_80161DC8_1629C8 == 2) {
            func_80034B68_35768(M2C_FIELD(temp_s0, s32 *, 0xC));
        }
        M2C_FIELD(temp_s0, s32 *, 0) = 0;
        M2C_FIELD(temp_s0, s32 *, 0xC) = 0;
    }
    if ((f64) M2C_FIELD(sp20, f32 *, 0x10) <= -8.0) {
        func_80034B90_35790();
        func_80034E8C_35A8C(&func_801D1FCC_5FCA4C);
    }
}
