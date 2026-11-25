typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_801DA314_604D94(s32, M2C_UNK);
M2C_UNK func_80205DB4_630834(void *);
M2C_UNK func_802097AC_63422C(void *);
M2C_UNK func_80209D54_6347D4();
extern void *func_80214670_5CFC00;

void func_80205E28_6308A8(void *arg0, s32 arg1) {
    s32 temp_t7;

    func_80209D54_6347D4();
    func_801DA314_604D94(arg1 + 8, 0x40800000);
    if (--M2C_FIELD(arg0, s32 *, 0x7C) == 0) {
        M2C_FIELD(func_80214670_5CFC00, s8 *, 4) = 0;
        func_80205DB4_630834(arg0);
    }
    func_802097AC_63422C(arg0);
}
