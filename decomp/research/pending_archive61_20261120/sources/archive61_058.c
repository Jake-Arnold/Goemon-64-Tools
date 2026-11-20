typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
extern f64 D_08003278_6F3488;

s32 func_080017A4_6F19B4(void *arg0) {
    if (D_08003278_6F3488 < (f64) M2C_FIELD(arg0, f32 *, 0xDC)) {
        return 1;
    }
    return 0;
}
