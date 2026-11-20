typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
M2C_UNK osPfsIsPlug(M2C_UNK *, s32);                /* extern */
extern M2C_UNK D_80167170_167D70;

void func_801CB848_6A9D08(s32 arg0) {
    osPfsIsPlug(&D_80167170_167D70, arg0);
}
