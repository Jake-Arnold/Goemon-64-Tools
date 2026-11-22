typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8003521C_35E1C();
extern s32 func_80200818_62BBF8();
void func_802007D4_62BBB4(void *arg0, void *arg1) {
    func_8003521C_35E1C(&func_80200818_62BBF8);
    (*(f32*)((u8*)(arg0) + 0x90)) = (f32) (*(f32*)((u8*)(arg1) + 0x8));
    (*(f32*)((u8*)(arg0) + 0x94)) = (f32) (*(f32*)((u8*)(arg1) + 0x10));
}
