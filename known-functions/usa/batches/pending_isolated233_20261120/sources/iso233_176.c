typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8003521C_35E1C();
extern s32 func_802034C4_62E8A4();
extern s32 func_802035D0_62E9B0();
extern s32 func_8020386C_62EC4C();
extern s32 func_80203F88_62F368();
extern s32 func_802043E4_62F7C4();
extern s32 D_8020EF40_63A320;
void func_80203424_62E804(void *arg0, void *arg1) {
    func_80203F88_62F368();
    if ((*(u8*)((u8*)(D_8020EF40_63A320) + 0x7)) != 0) {
        func_802035D0_62E9B0(arg0, (*(u8*)((u8*)(arg0) + 0x93)));
        func_8020386C_62EC4C(arg0, (*(u8*)((u8*)(arg0) + 0x93)));
    }
    if (func_802043E4_62F7C4(arg0) != 0) {
        (*(u8*)((u8*)(arg0) + 0x30)) = 0;
        (*(s32*)((u8*)(arg1) + 0x2C)) = 0;
        (*(s32*)((u8*)(arg0) + 0x7C)) = 0x50;
        (*(s32*)((u8*)(arg0) + 0x80)) = 1;
        (*(u8*)((u8*)(D_8020EF40_63A320) + 0x8)) = (u8) ((*(u8*)((u8*)(D_8020EF40_63A320) + 0x8)) + 1);
        func_8003521C_35E1C(&func_802034C4_62E8A4);
    }
}
