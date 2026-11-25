typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80034E8C_35A8C(s32);
f32 func_801D8660_6030E0(void *, f32);
s32 func_801D9238_603CB8(void *, f32, u16);
void func_801D9620_6040A0(void *, u16, s32);
void func_801FDE40_6288C0(void *, f32);
M2C_UNK func_801FCA5C_6274DC(void *);
extern f64 D_80213DA0_63E820;
extern M2C_UNK func_801F8A4C_6234CC;

void func_801F8984_623404(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    func_801D9238_603CB8(arg0, M2C_FIELD(arg1, f32 *, 0x20) * 300.0f, 0x10U);
    func_801D9620_6040A0(arg0, 0U, 8);
    func_801FCA5C_6274DC(arg0);
    if (func_801D8660_6030E0(arg1, 50.0f) == 0.0f) {
        func_801FDE40_6288C0(arg0, (f32) ((f64) M2C_FIELD(arg1, f32 *, 0x20) * D_80213DA0_63E820));
        M2C_FIELD(arg0, s32 *, 0x7C) = 0xC8;
        M2C_FIELD(arg0, f32 *, 0x90) = 0.0f;
        func_80034E8C_35A8C((s32) &func_801F8A4C_6234CC);
    }
}
