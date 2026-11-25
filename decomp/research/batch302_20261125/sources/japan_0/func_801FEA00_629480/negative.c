typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80034B44_35744(void);
s32 func_8000E15C_ED5C(f32, f32, f32, f32, void *);
void func_80038838_39438(s32);
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
extern void *D_80214600_63F080;
extern M2C_UNK func_801FEA80_629500;

void func_801FEA00_629480(void *arg0, M2C_UNK arg1) {
    volatile int negative_control = 1;

    if (M2C_FIELD(M2C_FIELD(D_80214600_63F080, void **, 0x1D8), s32 *, 0xD8) != 0x16) {
        func_80034B44_35744();
        return;
    }
    M2C_FIELD(arg0, s32 *, 0x7C) = 0x10;
    func_8000E15C_ED5C(6.0f, 0.0f, 0.0f, 0.0f, arg0);
    func_80034E8C_35A8C(&func_801FEA80_629500);
    func_80038838_39438(0x22E);
}
