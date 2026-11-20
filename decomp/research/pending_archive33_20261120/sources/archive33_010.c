typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
void func_801D4400_643250(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s8 *, 0x9D) = 1;
    M2C_FIELD(arg0, s16 *, 0xB6) = 8;
}
