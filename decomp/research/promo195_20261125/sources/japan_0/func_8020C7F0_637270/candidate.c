typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_8000E15C_ED5C(f32, f32, f32, f32, void *);
void func_80034E8C_35A8C(s32);
void func_801DB86C_6062EC(void *);
void func_8020CC1C_63769C(void *);
void func_8020CDC8_637848(void *);
extern f32 D_802145B8_63F038;
extern M2C_UNK func_8020C888_637308;

void func_8020C7F0_637270(void *arg0, void *arg1) {
    if (M2C_FIELD(arg0, s32 *, 0x7C) < 0x14) {
        func_801DB86C_6062EC(arg0);
    }
    if (D_802145B8_63F038 <= M2C_FIELD(arg1, f32 *, 0x10)) {
        func_8000E15C_ED5C(8.0f, 0.0f, 0.0f, 80.0f, arg0);
        func_80034E8C_35A8C((s32) &func_8020C888_637308);
    }
    func_8020CDC8_637848(arg0);
    func_8020CC1C_63769C(arg0);
}
