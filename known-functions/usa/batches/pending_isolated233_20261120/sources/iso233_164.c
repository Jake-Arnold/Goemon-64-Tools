typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8003522C_35E2C();
extern s32 func_801D31CC_5FE5AC();
extern s32 func_801FBD6C_62714C();
extern s32 func_801FFDFC_62B1DC();
extern s32 D_8020B3F0_6367D0;
void func_801FC3FC_6277DC(void *arg0) {
    (*(s32*)((u8*)(arg0) + 0xD8)) = 0;
    (*(s32*)((u8*)(arg0) + 0xE0)) = 0;
    (*(u8*)((u8*)(arg0) + 0x30)) = 1;
    (*(s32*)((u8*)(arg0) + 0x48)) = 0;
    (*(u8*)((u8*)(arg0) + 0x4C)) = 0;
    func_801FFDFC_62B1DC();
    func_801D31CC_5FE5AC(arg0, &D_8020B3F0_6367D0);
    func_8003522C_35E2C(arg0, &func_801FBD6C_62714C);
}
