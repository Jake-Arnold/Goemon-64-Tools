typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8003521C_35E1C();
extern s32 func_80037C20_38820();
extern s32 func_80037C9C_3889C();
extern s32 func_80038BC8_397C8();
extern s32 func_80201B38_62CF18();
void func_80201AD4_62CEB4(void *arg0, s32 arg1) {
    (*(s32*)((u8*)(arg0) + 0x7C)) = 0x64;
    (*(s32*)((u8*)(arg0) + 0x80)) = 1;
    func_8003521C_35E1C(&func_80201B38_62CF18);
    func_80038BC8_397C8(0x169);
    func_80037C9C_3889C(0, 0x64);
    func_80037C20_38820(0, 1, 0x11111111);
}
