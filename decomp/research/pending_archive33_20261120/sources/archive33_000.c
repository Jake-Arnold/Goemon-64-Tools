typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
void func_80012470_13070(void *arg0) {
    M2C_FIELD(arg0, s16 *, 0xCA) = 0;
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x9C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0xAC) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0xA4) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0xB4) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0xC4) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0xBC) = 0.0f;
    M2C_FIELD(arg0, s16 *, 0xC8) = (s16) M2C_FIELD(arg0, s16 *, 0xCA);
}
