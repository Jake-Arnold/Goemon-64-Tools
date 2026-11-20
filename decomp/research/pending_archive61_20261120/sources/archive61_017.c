typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
extern s32 D_80168F60_169B60;
extern s32 D_80168F64_169B64;
extern M2C_UNK D_8020EEE0;

void func_801D2BF0_5FDFD0(void) {
    D_80168F60_169B60 = 0;
    D_80168F64_169B64 = 0;
    M2C_FIELD(&D_8020EEE0, s32 *, 0) = 0;
    M2C_FIELD(&D_8020EEE0, s32 *, 4) = 0;
    M2C_FIELD(&D_8020EEE0, s32 *, 8) = 0;
    M2C_FIELD(&D_8020EEE0, s32 *, 0xC) = 0;
    M2C_FIELD(&D_8020EEE0, s32 *, 0x10) = 0;
    M2C_FIELD(&D_8020EEE0, s32 *, 0x14) = 0;
}
