typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
M2C_UNK func_800239B8_245B8(s32);                   /* static */
extern s32 D_801C7740_1C8340;

void func_80023DC4_249C4(void) {
    func_800239B8_245B8(D_801C7740_1C8340);
}
