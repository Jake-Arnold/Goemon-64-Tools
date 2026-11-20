typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_800109A4_115A4();
extern s32 func_800114B8_120B8();
extern s32 func_800119D4_125D4();
extern s32 func_8001B6A4_1C2A4();
extern s32 func_800232EC_23EEC();
extern s32 func_8003521C_35E1C();
extern s32 func_801CB460_65E310();
extern s32 func_801CF2E0_662190();
extern s32 D_801D4CE8_667B98;
extern s32 D_801E86F0_67B5A0;
void func_801CCAA4_65F954(void *arg0, s32 arg1) {
    func_800232EC_23EEC();
    func_801CB460_65E310();
    func_800109A4_115A4(D_801D4CE8_667B98, 0);
    func_8001B6A4_1C2A4(0x64, 0x64, 0x64);
    D_801E86F0_67B5A0 = func_800114B8_120B8(arg0, 2, 0);
    (*(s32*)((u8*)(arg0) + 0xA4)) = func_800119D4_125D4(arg0, 0xB);
    func_8003521C_35E1C(&func_801CF2E0_662190);
}
