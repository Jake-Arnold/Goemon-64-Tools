#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
void func_08004FDC_6C472C(void *arg0, void *arg1) {
    M2C_FIELD(arg1, u16 *, 0x16) = (u16) ((M2C_FIELD(arg1, u16 *, 0x16) + 2) & 0x3FF);
    if (M2C_FIELD(arg1, f32 *, 0xC) > 80.0f) {
        M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    }
}
