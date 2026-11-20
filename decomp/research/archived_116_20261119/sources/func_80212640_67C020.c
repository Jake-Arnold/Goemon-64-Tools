typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
extern void *D_801FC60C_5B851C;
extern void *D_801FC61C_5B852C;

void func_80212640_67C020(s32 arg0) {
    M2C_FIELD(D_801FC60C_5B851C, s8 *, 0x64) = 1;
    M2C_FIELD(D_801FC61C_5B852C, s8 *, 0x64) = 1;
}
