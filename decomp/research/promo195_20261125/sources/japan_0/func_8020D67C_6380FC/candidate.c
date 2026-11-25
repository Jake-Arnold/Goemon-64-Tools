typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80034E8C_35A8C(s32);
void func_80034E9C_35A9C(void *, s32);
void func_80038838_39438(s32);
s32 func_801DA42C_604EAC(f32, f32, f32, f32);
void func_801E98C4_614344(s32, s32, s32, s32);
extern s32 D_80214600_63F080;
extern M2C_UNK func_80208140_632BC0;
extern M2C_UNK func_80208420_632EA0;
extern M2C_UNK func_8020D72C_6381AC;

void func_8020D67C_6380FC(void *arg0, M2C_UNK arg1) {
    void *sp1C;

    sp1C = D_80214600_63F080 + 0x178;
    if (func_801DA42C_604EAC(1.5f, -250.0f, -100.0f, 0.0f) != 0) {
        func_80038838_39438(0x17B);
        func_801E98C4_614344(0xFF, 0xFF, 0xFF, 0xFF);
        func_80034E9C_35A9C(M2C_FIELD(sp1C, void **, 0x20), (s32) &func_80208140_632BC0);
        func_80034E9C_35A9C(M2C_FIELD(sp1C, void **, 0x24), (s32) &func_80208420_632EA0);
        M2C_FIELD(arg0, s32 *, 0x7C) = 0;
        M2C_FIELD(arg0, s32 *, 0x90) = 0;
        func_80034E8C_35A8C((s32) &func_8020D72C_6381AC);
    }
}
