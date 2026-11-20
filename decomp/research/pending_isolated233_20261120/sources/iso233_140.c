typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8003521C_35E1C();
extern s32 func_80038BC8_397C8();
extern s32 func_801D2EE4_5FE2C4();
extern s32 func_801D34D0_5FE8B0();
extern s32 func_801E8220_613600();
extern s32 D_8020B094_636474;
extern s32 D_8020B180_636560;
extern s32 D_8020B190_636570;
void func_801E818C_61356C(void *arg0, void *arg1) {
    (*(s32*)((u8*)(arg0) + 0xB0)) = 1;
    func_80038BC8_397C8(0x823E);
    func_80038BC8_397C8(0x8240);
    func_80038BC8_397C8(0x8241);
    if ((s32) (*(u16*)((u8*)(arg1) + 0x16)) < 0x201) {
        func_801D2EE4_5FE2C4(arg1, &D_8020B190_636570);
    } else {
        func_801D2EE4_5FE2C4(arg1, &D_8020B180_636560);
    }
    func_801D34D0_5FE8B0(arg1, &D_8020B094_636474, 0, 1);
    func_8003521C_35E1C(&func_801E8220_613600);
}
