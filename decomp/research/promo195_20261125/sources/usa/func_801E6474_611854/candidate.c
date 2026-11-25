typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_8003521C_35E1C(s32);
void func_80038BC8_397C8(s32);
void func_801D2EE4_5FE2C4(void *, void *);
f32 func_801D31F0_5FE5D0(void *, f32);
void func_801D34D0_5FE8B0(void *, s32, s32, s32);
s32 func_801D3B18_5FEEF8(void *, f32, u16);
void func_801D3F00_5FF2E0(void *, u16, s32);
extern M2C_UNK D_8020B094_636474;
extern M2C_UNK D_8020B1C0_6365A0;
extern M2C_UNK func_801E651C_6118FC;

void func_801E6474_611854(void *arg0, void *arg1) {
    func_801D3B18_5FEEF8(arg0, 80.0f, 0xAU);
    func_801D3F00_5FF2E0(arg0, 0U, 8);
    if (func_801D31F0_5FE5D0(arg0, 20.0f) == 0.0f) {
        func_80038BC8_397C8(0x235);
        func_801D2EE4_5FE2C4(arg1, &D_8020B1C0_6365A0);
        func_801D34D0_5FE8B0(arg1, (s32) &D_8020B094_636474, 0, 0);
        func_8003521C_35E1C((s32) &func_801E651C_6118FC);
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x14;
    }
}
