typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
extern s32 D_80152C38_153838;
void func_800086C4_92C4(void *arg0, s32 arg1, s32 arg2) {
    (*(s32*)((u8*)(arg0) + 0x34)) = arg1;
    (*(s32*)((u8*)(arg0) + 0x14)) = arg2;
    D_80152C38_153838 = arg2;
}
