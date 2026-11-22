typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
extern s32 D_801FC7C4_5B86D4;
extern s32 D_801FC61C_5B852C;
void func_801E0794_59C6A4(s32 arg0, void *arg1) {
    (*(u8*)((u8*)(D_801FC61C_5B852C) + 0x64)) = 1;
    D_801FC7C4_5B86D4 = 0;
    func_801DD720_599630(arg0, 5);
    if ((f64) (*(f32*)((u8*)(arg1) + 0x28)) <= 0.0) {
        func_801E6E98_5A2DA8(arg0);
        func_801DACDC_596BEC(arg0, 0x38);
    }
}
