typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80034B44_35744(void);
void func_80034E8C_35A8C(s32);
void func_801D8DE4_603864(void *);
extern void *D_80214600_63F080;
extern M2C_UNK func_801FEA00_629480;
extern M2C_UNK func_801FEC38_6296B8;

void func_801FEB94_629614(void *arg0, M2C_UNK arg1) {
    s32 temp_t0;
    s32 temp_t3;

    if (M2C_FIELD(M2C_FIELD(D_80214600_63F080, void **, 0x1D8), s32 *, 0xD8) != 0x16) {
        func_80034B44_35744();
        return;
    }
    if (--M2C_FIELD(arg0, s32 *, 0x7C) == 0) {
        if (++M2C_FIELD(arg0, s32 *, 0x90) != 2) {
            func_801D8DE4_603864(arg0);
            func_80034E8C_35A8C((s32) &func_801FEA00_629480);
            return;
        }
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x14;
        func_80034E8C_35A8C((s32) &func_801FEC38_6296B8);
    }
}
