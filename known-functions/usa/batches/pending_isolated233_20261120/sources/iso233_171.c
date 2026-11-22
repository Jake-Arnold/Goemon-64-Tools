typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8003521C_35E1C();
extern s32 func_80200BE8_62BFC8();
extern s32 func_8020407C_62F45C();
extern s32 D_8020EF40_63A320;
void func_80200BA4_62BF84(s32 arg0, s32 arg1) {
    (*(u8*)((u8*)(D_8020EF40_63A320) + 0x5)) = 1;
    func_8003521C_35E1C(&func_80200BE8_62BFC8);
    func_8020407C_62F45C(arg0);
}
