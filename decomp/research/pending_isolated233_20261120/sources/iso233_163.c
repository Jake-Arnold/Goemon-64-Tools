typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8003521C_35E1C();
extern s32 func_80038BC8_397C8();
extern s32 func_801D31CC_5FE5AC();
extern s32 func_801FBC2C_62700C();
extern s32 func_801FFE14_62B1F4();
extern s32 func_801FFE6C_62B24C();
extern s32 D_8020EF40_63A320;
extern s32 D_8020B3F0_6367D0;
void func_801FBBBC_626F9C(void *arg0, s32 arg1) {
    func_801FFE6C_62B24C();
    (*(u8*)((u8*)(D_8020EF40_63A320) + 0x815)) = 0;
    (*(u8*)((u8*)(D_8020EF40_63A320) + 0x817)) = 0;
    func_80038BC8_397C8(0x8152);
    func_801FFE14_62B1F4();
    (*(s32*)((u8*)(arg0) + 0xE0)) = 0;
    (*(s32*)((u8*)(arg0) + 0xD8)) = 0;
    func_801D31CC_5FE5AC(arg0, &D_8020B3F0_6367D0);
    func_8003521C_35E1C(&func_801FBC2C_62700C);
}
