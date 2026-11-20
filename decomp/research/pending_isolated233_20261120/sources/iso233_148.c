typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8003521C_35E1C();
extern s32 func_801D3018_5FE3F8();
extern s32 func_801F0414_61B7F4();
extern s32 func_801F7074_622454();
extern s32 func_801F732C_62270C();
void func_801F03C4_61B7A4(void *arg0, s32 arg1) {
    func_801F7074_622454();
    func_801D3018_5FE3F8(arg1, 0x42200000);
    if (func_801F732C_62270C(arg0) != 0) {
        (*(s32*)((u8*)(arg0) + 0x7C)) = 0;
        func_8003521C_35E1C(&func_801F0414_61B7F4);
    }
}
