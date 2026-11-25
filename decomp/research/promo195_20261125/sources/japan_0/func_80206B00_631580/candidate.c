typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80034E8C_35A8C(s32);
void func_80205DB4_630834(void *);
s32 func_802097AC_63422C(void *);
extern void *func_80214670_5CFC00;
extern M2C_UNK func_80206B6C_6315EC;

void func_80206B00_631580(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x7C) = 0xC8;
    func_80034E8C_35A8C((s32) &func_80206B6C_6315EC);
    if (M2C_FIELD(func_80214670_5CFC00, u8 *, 0x10) != 0) {
        func_80205DB4_630834(arg0);
        return;
    }
    func_802097AC_63422C(arg0);
}
