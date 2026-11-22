typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8003521C_35E1C();
extern s32 func_802006F8_62BAD8();
extern s32 func_8020407C_62F45C();
void func_802006BC_62BA9C(void *arg0, s32 arg1) {
    (*(s32*)((u8*)(arg0) + 0x7C)) = 0xFA;
    func_8003521C_35E1C(&func_802006F8_62BAD8);
    func_8020407C_62F45C(arg0);
}
