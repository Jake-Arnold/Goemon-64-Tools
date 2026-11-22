typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8003521C_35E1C();
extern s32 func_801D2EE4_5FE2C4();
extern s32 func_801F4654_61FA34();
extern s32 func_801F7074_622454();
extern s32 func_801F76D0_622AB0();
extern s32 D_8020B2B8_636698;
extern s32 D_8020B2C0_6366A0;
void func_801F45E8_61F9C8(s32 arg0, void *arg1) {
    func_801F7074_622454();
    func_801F76D0_622AB0(arg0);
    if ((s32) (*(u16*)((u8*)(arg1) + 0x16)) < 0x201) {
        func_801D2EE4_5FE2C4(arg1, &D_8020B2C0_6366A0);
    } else {
        func_801D2EE4_5FE2C4(arg1, &D_8020B2B8_636698);
    }
    func_8003521C_35E1C(&func_801F4654_61FA34);
}
