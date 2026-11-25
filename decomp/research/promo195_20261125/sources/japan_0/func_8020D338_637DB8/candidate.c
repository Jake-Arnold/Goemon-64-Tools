typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80034E8C_35A8C(s32);
s32 func_801DA42C_604EAC(f32, f32, f32, f32);
void func_801E98C4_614344(s32, s32, s32, s32);
extern void *D_80214600_63F080;
extern M2C_UNK func_8020D3BC_637E3C;

void func_8020D338_637DB8(void *arg0, M2C_UNK arg1) {
    if ((M2C_FIELD(D_80214600_63F080, u8 *, 0x2C1) == 2) && (func_801DA42C_604EAC(1.0f, 0.0f, 0.0f, 0.0f) != 0)) {
        func_801E98C4_614344(0xFF, 0xFF, 0xFF, 0xFF);
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x64;
        func_80034E8C_35A8C((s32) &func_8020D3BC_637E3C);
    }
}
