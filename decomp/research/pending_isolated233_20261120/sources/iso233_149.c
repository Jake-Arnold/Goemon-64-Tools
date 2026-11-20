typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8003521C_35E1C();
extern s32 func_801D31CC_5FE5AC();
extern s32 func_801F060C_61B9EC();
extern s32 func_801F7074_622454();
extern s32 D_8020B268_636648;
void func_801F05BC_61B99C(void *arg0, s32 arg1) {
    func_801F7074_622454();
    func_801D31CC_5FE5AC(arg0, &D_8020B268_636648);
    (*(f32*)((u8*)(arg0) + 0x74)) = 1.0f;
    func_8003521C_35E1C(&func_801F060C_61B9EC);
}
