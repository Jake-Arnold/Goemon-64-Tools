typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_8003521C_35E1C(s32);
void func_8003522C_35E2C(void *, s32);
void func_80038BC8_397C8(s32);
s32 func_801D4D0C_6000EC(f32, f32, f32, f32);
void func_801E4194_60F574(s32, s32, s32, s32);
extern s32 D_8020EED0_63A2B0;
extern M2C_UNK func_80202A10_62DDF0;
extern M2C_UNK func_80202CF0_62E0D0;
extern M2C_UNK func_80207FFC_6333DC;

void func_80207F4C_63332C(void *arg0, M2C_UNK arg1) {
    void *sp1C;

    sp1C = D_8020EED0_63A2B0 + 0x178;
    if (func_801D4D0C_6000EC(1.5f, -250.0f, -100.0f, 0.0f) != 0) {
        func_80038BC8_397C8(0x17B);
        func_801E4194_60F574(0xFF, 0xFF, 0xFF, 0xFF);
        func_8003522C_35E2C(M2C_FIELD(sp1C, void **, 0x20), (s32) &func_80202A10_62DDF0);
        func_8003522C_35E2C(M2C_FIELD(sp1C, void **, 0x24), (s32) &func_80202CF0_62E0D0);
        M2C_FIELD(arg0, s32 *, 0x7C) = 0;
        M2C_FIELD(arg0, s32 *, 0x90) = 0;
        func_8003521C_35E1C((s32) &func_80207FFC_6333DC);
    }
}
