typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8003521C_35E1C();
extern s32 func_801D2EE4_5FE2C4();
extern s32 func_801F5710_620AF0();
extern s32 func_801F7074_622454();
extern s32 D_8020B2C8_6366A8;
void func_801F56C8_620AA8(void *arg0, s32 arg1) {
    func_801F7074_622454();
    func_801D2EE4_5FE2C4(arg1, &D_8020B2C8_6366A8);
    func_8003521C_35E1C(&func_801F5710_620AF0);
    (*(s32*)((u8*)(arg0) + 0x90)) = 0;
}
