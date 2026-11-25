typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80034E8C_35A8C(s32);
void func_801D8604_603084(void *, void *);
f32 func_801D8660_6030E0(void *, f32);
s32 func_801D9138_603BB8(void);
void func_801DB804_606284(void *);
void func_801DBC28_6066A8(void *, f32);
void func_80205544_62FFC4(void);
void func_80205584_630004(void);
extern M2C_UNK D_80210B70_63B5F0;
extern M2C_UNK func_80203AF0_62E570;

void func_80203A38_62E4B8(void *arg0, void *arg1) {
    s32 temp_t9;

    func_801D8660_6030E0(arg1, (f32) M2C_FIELD(arg0, s32 *, 0x80));
    M2C_FIELD(arg0, s32 *, 0xE0) = 2;
    if (func_801D9138_603BB8() != 0) {
        func_80205544_62FFC4();
    } else {
        func_80205584_630004();
    }
    func_801DB804_606284(arg0);
    func_801DBC28_6066A8(arg0, -0.2f);
    if (--M2C_FIELD(arg0, s32 *, 0x7C) <= 0) {
        func_801D8604_603084(arg1, &D_80210B70_63B5F0);
        func_80034E8C_35A8C((s32) &func_80203AF0_62E570);
    }
}
