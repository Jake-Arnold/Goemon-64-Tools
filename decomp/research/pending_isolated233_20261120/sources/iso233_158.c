typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 D_8020EED0_63A2B0;
void func_801FADC0_6261A0(s32 arg0) {
    void *temp_v0;

    temp_v0 = (*(s32*)((u8*)(D_8020EED0_63A2B0) + 0x1DC));
    if (temp_v0 != NULL) {
        (*(s32*)((u8*)(temp_v0) + 0x80)) = arg0;
    }
}
