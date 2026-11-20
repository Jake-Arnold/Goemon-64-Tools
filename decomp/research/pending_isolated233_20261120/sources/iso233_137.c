typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8003521C_35E1C();
extern s32 func_801D31CC_5FE5AC();
extern s32 func_801D34D0_5FE8B0();
extern s32 func_801E607C_61145C();
extern s32 func_801EF2B0_61A690();
extern s32 D_8020B178_636558[];
extern s32 D_8020B094_636474[];
void func_801E6024_611404(s32 arg0, s32 arg1) {
    func_801EF2B0_61A690();
    func_801D31CC_5FE5AC(arg0, &D_8020B178_636558);
    func_801D34D0_5FE8B0(arg1, &D_8020B094_636474, 0, 0);
    func_8003521C_35E1C(&func_801E607C_61145C);
}
