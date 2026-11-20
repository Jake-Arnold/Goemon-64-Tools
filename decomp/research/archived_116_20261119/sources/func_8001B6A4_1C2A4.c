typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
extern M2C_UNK D_8006B6A8_6C2A8;

void func_8001B6A4_1C2A4(s8 arg0, s8 arg1, s8 arg2) {
    M2C_FIELD(&D_8006B6A8_6C2A8, s8 *, 4) = arg0;
    M2C_FIELD(&D_8006B6A8_6C2A8, s8 *, 0) = arg0;
    M2C_FIELD(&D_8006B6A8_6C2A8, s8 *, 5) = arg1;
    M2C_FIELD(&D_8006B6A8_6C2A8, s8 *, 1) = arg1;
    M2C_FIELD(&D_8006B6A8_6C2A8, s8 *, 6) = arg2;
    M2C_FIELD(&D_8006B6A8_6C2A8, s8 *, 2) = arg2;
}
