#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
extern M2C_UNK D_8015CC30_15D830;

void func_80220FF0_5DC4C0(void *arg0) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    M2C_FIELD(arg0, s32 *, 0xB4) = (s32) M2C_FIELD(arg0, s32 *, 0xC);
    M2C_FIELD(&D_8015CC30_15D830, u16 *, 0x14E) = (u16) M2C_FIELD(temp_v0, u16 *, 0x16);
    M2C_FIELD(&D_8015CC30_15D830, s32 *, 0x150) = (s32) M2C_FIELD(temp_v0, s32 *, 0x2C);
    M2C_FIELD(&D_8015CC30_15D830, u16 *, 0x154) = (u16) M2C_FIELD(temp_v0, u16 *, 0x7E);
    M2C_FIELD(&D_8015CC30_15D830, s16 *, 0x156) = (s16) M2C_FIELD(temp_v0, u8 *, 0x7C);
}
