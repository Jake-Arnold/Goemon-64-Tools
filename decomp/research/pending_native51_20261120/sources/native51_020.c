#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
extern s32 D_8015C5C8_15D1C8;

void func_80224440_5DF910(s32 arg0) {
    s32 temp_v0;

    temp_v0 = arg0 * 0x18;
    M2C_FIELD((D_8015C5C8_15D1C8 + temp_v0), s16 *, 0x3B0F2) = 0;
    M2C_FIELD((D_8015C5C8_15D1C8 + temp_v0), s16 *, 0x3B0F4) = 0;
    M2C_FIELD((D_8015C5C8_15D1C8 + temp_v0), s16 *, 0x3B0F6) = 0;
    M2C_FIELD((D_8015C5C8_15D1C8 + temp_v0), s16 *, 0x3B0F8) = 0;
}
