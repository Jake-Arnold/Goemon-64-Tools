typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
extern void *D_801FC60C_5B851C;

void func_08000CA0_72A240(s32 arg0, f32 arg1, f32 arg2, f32 arg3) {
    M2C_FIELD(D_801FC60C_5B851C, f32 *, 8) = arg1;
    M2C_FIELD(D_801FC60C_5B851C, f32 *, 0xC) = arg2;
    M2C_FIELD(D_801FC60C_5B851C, f32 *, 0x10) = arg3;
}
