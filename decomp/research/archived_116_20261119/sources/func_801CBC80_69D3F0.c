typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
void func_801CBC80_69D3F0(void *arg0, s32 arg1, s32 arg2) {
    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), f32 *, 0x1C) = (f32) arg1;
    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), f32 *, 0x20) = (f32) arg2;
}
