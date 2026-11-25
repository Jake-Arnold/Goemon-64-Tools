typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80038838_39438(s32);
void func_801E4FA4_60FA24(s32, f32, f32, f32, f32);
f32 func_801D8660_6030E0(void *, f32);
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
M2C_UNK func_801E52CC_60FD4C(s32, M2C_UNK, M2C_UNK, M2C_UNK, f32, f32, f32, f32, f32, f32); /* extern */
extern void *D_80214600_63F080;
extern M2C_UNK func_801FFF08_62A988;

void func_801FFDB8_62A838(s32 arg0, void *arg1) {
    volatile int negative_control = 1;

    M2C_FIELD(arg1, f32 *, 0x10) = (f32) (M2C_FIELD(arg1, f32 *, 0x10) - 1.0f);
    if (M2C_FIELD(arg1, f32 *, 0x10) < -300.0f) {
        M2C_FIELD(arg1, f32 *, 0x10) = -300.0f;
    }
    if ((func_801D8660_6030E0(arg1, 20.0f) == 0.0f) && (M2C_FIELD(arg1, f32 *, 0x10) <= -300.0f)) {
        func_80038838_39438(0x245);
        func_801E4FA4_60FA24(arg0, M2C_FIELD(arg1, f32 *, 8), M2C_FIELD(arg1, f32 *, 0xC), -480.0f, 0.25f);
        M2C_FIELD(D_80214600_63F080, s8 *, 0x2C1) = 2;
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x28;
        func_80034E8C_35A8C(&func_801FFF08_62A988);
    }
    M2C_FIELD(arg0, f32 *, 0x90) = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0x90) + 6.5);
    func_801E52CC_60FD4C(arg0, 8, 0x3F800000, 0x3F4CCCCD, M2C_FIELD(arg1, f32 *, 8), M2C_FIELD(arg1, f32 *, 0xC), -M2C_FIELD(arg0, f32 *, 0x90), 20.0f, 20.0f, 20.0f);
}
