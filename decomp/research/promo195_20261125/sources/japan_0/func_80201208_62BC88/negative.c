typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80034E8C_35A8C(s32);
f32 func_801D8660_6030E0(void *, f32);
u8 func_801DC2AC_606D2C(s32, M2C_UNK);
extern void *D_80214600_63F080;
extern M2C_UNK func_802012A4_62BD24;

void func_80201208_62BC88(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_t7;

    func_801D8660_6030E0(arg1, 100.0f);
    if (--M2C_FIELD(arg0, s32 *, 0x7C) == 0) {
        M2C_FIELD(D_80214600_63F080, s8 *, 0x2C1) = 3;
        func_80034E8C_35A8C((s32) &func_802012A4_62BD24);
        return;
    }
    func_801DC2AC_606D2C((s32) arg0, 0x3E4CCCCD);
    M2C_FIELD(arg1, f32 *, 0x10) = (f32) ((f64) M2C_FIELD(arg1, f32 *, 0x10) - 0.5);
}
