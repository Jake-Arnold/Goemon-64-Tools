typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
extern f32 D_80217BA8_676B58;

void func_80214E38_673DE8(void *arg0) {
    M2C_FIELD(arg0, f32 *, 0xB4) = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0xA4) + 100.0);
    M2C_FIELD(arg0, f32 *, 0xB0) = (f32) D_80217BA8_676B58;
}
