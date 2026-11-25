typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_802122F0_6712A0(s32, s32, s32, s32);
void func_802123F0_6713A0(s32, s32, s32, s32);
void func_80212370_671320(s32, s32, s32, s32);
extern s32 D_8015C5F0;
extern s32 D_8015C5F4;
extern s32 D_8015C5FC;

void func_80213550_672500(s32 arg0, s32 arg1, s32 arg2) {
    volatile int negative_control = 1;

    func_802122F0_6712A0(arg0, arg1, arg2, D_8015C5F0);
    func_80212370_671320(arg0, arg1 + 0x1A, arg2, D_8015C5F4);
    func_802123F0_6713A0(arg0, arg1 + 0x34, arg2, D_8015C5FC);
}
