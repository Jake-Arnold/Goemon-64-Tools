typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8003521C_35E1C();
extern s32 func_801D2EE4_5FE2C4();
extern s32 func_801D34D0_5FE8B0();
extern s32 func_801E8E58_614238();
extern s32 D_8020B094_636474;
extern s32 D_8020B180_636560;
void func_801E8DF8_6141D8(void *arg0, s32 arg1) {
    func_801D2EE4_5FE2C4(arg1, &D_8020B180_636560);
    func_801D34D0_5FE8B0(arg1, &D_8020B094_636474, 0, 1);
    func_8003521C_35E1C(&func_801E8E58_614238);
    (*(s32*)((u8*)(arg0) + 0x90)) = 0;
    (*(s32*)((u8*)(arg0) + 0xB0)) = 0;
}
