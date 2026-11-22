typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8003521C_35E1C();
extern s32 func_801D2F40_5FE320();
extern s32 func_801D36C4_5FEAA4();
extern s32 func_801EC908_617CE8();
extern s32 func_801ECE48_618228();
extern s32 func_801ECEDC_6182BC();
void func_801EC85C_617C3C(void *arg0, void *arg1) {
    if ((func_801ECEDC_6182BC() == 0) && (func_801ECE48_618228(arg0) == 0)) {
        func_801D2F40_5FE320(arg1, 0x42700000);
        if ((f64) (*(f32*)((u8*)(arg1) + 0x28)) >= 22.0) {
            (*(f32*)((u8*)(arg1) + 0x28)) = 22.0f;
            (*(u8*)((u8*)(arg0) + 0x30)) = (u8) ((*(u8*)((u8*)(arg0) + 0x30)) | 2);
            func_801D36C4_5FEAA4(arg0);
            (*(s32*)((u8*)(arg0) + 0x80)) = 0xA;
            (*(s32*)((u8*)(arg0) + 0xB4)) = 0;
            func_8003521C_35E1C(&func_801EC908_617CE8);
        }
    }
}
