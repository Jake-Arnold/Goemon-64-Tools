#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
void func_801E32D4_59F1E4(void *arg0, f32 arg1, f32 arg2, f32 arg3) {
    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), f32 *, 4) = arg1;
    M2C_FIELD(arg0, f32 *, 0xE4) = arg2;
    M2C_FIELD(arg0, f32 *, 0xE8) = arg3;
    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0) = 1;
    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 2) = (s16) (M2C_FIELD(arg0, u16 *, 0x94) | 0x400);
    M2C_FIELD(arg0, f32 *, 0x68) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x6C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
}
