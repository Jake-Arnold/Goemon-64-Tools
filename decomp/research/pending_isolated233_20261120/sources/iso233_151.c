typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8003521C_35E1C();
extern s32 func_801F1788_61CB68();
extern s32 func_801F701C_6223FC();
extern s32 func_801F7074_622454();
void func_801F1738_61CB18(void *arg0, s32 arg1) {
    (*(f32*)((u8*)(arg0) + 0x70)) = 0.0f;
    (*(f32*)((u8*)(arg0) + 0x74)) = 0.0f;
    (*(f32*)((u8*)(arg0) + 0x78)) = -10.0f;
    func_801F701C_6223FC();
    func_801F7074_622454(arg0);
    func_8003521C_35E1C(&func_801F1788_61CB68);
}
