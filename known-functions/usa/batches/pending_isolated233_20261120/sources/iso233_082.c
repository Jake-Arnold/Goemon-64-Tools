typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
extern u8 D_8015C54D_15D14D;
extern s32 D_801FC61C_5B852C;
void func_801E5208_5A1118(void *arg0) {
    void *temp_v0;

    (*(s8*)((u8*)(D_801FC61C_5B852C) + 0x64)) = 1;
    temp_v0 = (*(s32*)((u8*)(arg0) + 0x5C));
    (*(u16*)((u8*)(temp_v0) + 0x30)) = (u16) ((*(u16*)((u8*)(temp_v0) + 0x30)) + 1);
    if ((s32) (*(u16*)((u8*)((*(void**)((u8*)(arg0) + 0x5C))) + 0x30)) >= 0x3C) {
        func_801E5090_5A0FA0();
        D_8015C54D_15D14D = 1;
        (*(u16*)((u8*)((*(void**)((u8*)(arg0) + 0x5C))) + 0x86)) = 0;
    }
}
