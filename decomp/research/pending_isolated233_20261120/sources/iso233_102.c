typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8003521C_35E1C();
extern s32 func_80214C0C_5D00DC();
extern s32 func_80216E1C_5D22EC();
extern s32 func_80221A90_5DCF60();
void func_80214BBC_5D008C(void *arg0, s32 arg1) {
    func_80221A90_5DCF60();
    (*(u8*)((u8*)(arg0) + 0x6C)) = 0;
    (*(s32*)((u8*)(arg0) + 0x60)) = (s32) ((*(s32*)((u8*)(arg0) + 0x60)) | 0x80000000);
    func_80216E1C_5D22EC(arg0, 0);
    func_8003521C_35E1C(&func_80214C0C_5D00DC);
}
