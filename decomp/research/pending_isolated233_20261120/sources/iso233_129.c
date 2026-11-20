typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_80013940_14540();
extern s32 func_8003521C_35E1C();
extern s32 func_801CB65C_5F6A3C();
extern s32 osViSetSpecialFeatures();
void func_801CB620_5F6A00(s32 arg0, s32 arg1) {
    osViSetSpecialFeatures(0x40);
    func_80013940_14540();
    func_8003521C_35E1C(&func_801CB65C_5F6A3C);
}
