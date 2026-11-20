typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8003521C_35E1C();
extern s32 func_801D2EE4_5FE2C4();
extern s32 func_801FE4D0_6298B0();
extern s32 func_801FFE6C_62B24C();
extern s32 D_8020B408_6367E8;
extern s32 D_8020EF40_63A320;
void func_801FE47C_62985C(void *arg0, s32 arg1) {
    func_801FFE6C_62B24C();
    (*(u8*)((u8*)(D_8020EF40_63A320) + 0x815)) = 0;
    func_801D2EE4_5FE2C4(arg1, &D_8020B408_6367E8);
    func_8003521C_35E1C(&func_801FE4D0_6298B0);
    (*(s32*)((u8*)(arg0) + 0x90)) = 0;
}
