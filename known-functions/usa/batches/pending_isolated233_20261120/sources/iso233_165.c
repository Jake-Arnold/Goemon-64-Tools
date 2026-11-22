typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8003521C_35E1C();
extern s32 func_80038BC8_397C8();
extern s32 func_801D2EE4_5FE2C4();
extern s32 func_801FE308_6296E8();
extern s32 func_801FFE6C_62B24C();
extern s32 D_8020EF40_63A320;
extern s32 D_8020B438_636818;
void func_801FE288_629668(void *arg0, s32 arg1) {
    func_801FFE6C_62B24C();
    (*(u8*)((u8*)(D_8020EF40_63A320) + 0x815)) = 0;
    (*(s32*)((u8*)(arg0) + 0x80)) = 0x92;
    (*(s32*)((u8*)(arg0) + 0x7C)) = 0x92;
    (*(f32*)((u8*)(arg0) + 0x74)) = 14.0f;
    func_801D2EE4_5FE2C4(arg1, &D_8020B438_636818);
    func_80038BC8_397C8(0x34E);
    (*(s32*)((u8*)(arg0) + 0xE8)) = (s32) ((*(s32*)((u8*)(arg0) + 0xE8)) + 1);
    func_8003521C_35E1C(&func_801FE308_6296E8);
}
