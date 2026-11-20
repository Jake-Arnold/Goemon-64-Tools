typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
void func_0800134C_730BDC(void *arg0, f32 arg1, f32 arg2, f32 arg3, f32 arg4) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0xD0);
    M2C_FIELD(temp_v0, s32 *, 0x10) = 1;
    M2C_FIELD(temp_v0, f32 *, 0x14) = arg1;
    M2C_FIELD(temp_v0, f32 *, 0x18) = arg2;
    M2C_FIELD(temp_v0, f32 *, 0x1C) = arg3;
    M2C_FIELD(temp_v0, f32 *, 0x20) = arg4;
}
