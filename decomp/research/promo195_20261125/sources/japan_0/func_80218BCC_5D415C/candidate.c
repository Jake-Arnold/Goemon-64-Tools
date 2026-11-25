typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80034E8C_35A8C(s32);
void func_8021BC40_5D71D0(void *, s32);
void func_8021EB78_5DA108(void *, f32);
extern M2C_UNK func_80218C5C_5D41EC;

void func_80218BCC_5D415C(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s32 *, 0x60) = 0x20;
    if (M2C_FIELD(arg0, u8 *, 0xD9) & 1) {
        M2C_FIELD(arg1, u16 *, 0x14) = 0x8000;
    }
    if (M2C_FIELD(arg0, u8 *, 0xD9) & 2) {
        M2C_FIELD(arg1, u16 *, 0x16) = 0x8000;
    }
    if (M2C_FIELD(arg0, u8 *, 0xD9) & 4) {
        M2C_FIELD(arg1, u16 *, 0x18) = 0x8000;
    }
    func_8021BC40_5D71D0(arg0, (s32) M2C_FIELD(arg0, u8 *, 0xD8));
    M2C_FIELD(arg1, s8 *, 0x65) = 0;
    func_8021EB78_5DA108(arg0, 10.0f);
    func_80034E8C_35A8C((s32) &func_80218C5C_5D41EC);
}
