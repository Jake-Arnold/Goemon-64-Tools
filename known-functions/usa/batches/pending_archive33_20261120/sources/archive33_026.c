typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
void func_08001860_7310F0(void *arg0, s32 arg1) {
    f32 temp_f0;
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, s32 *, 0xD4);
    temp_f0 = (f32) arg1;
    M2C_FIELD(arg0, s32 *, 0xE0) = temp_v0;
    M2C_FIELD(arg0, f32 *, 0xE4) = temp_f0;
    M2C_FIELD(arg0, f32 *, 0xE8) = (f32) (temp_f0 / (f32) temp_v0);
}
