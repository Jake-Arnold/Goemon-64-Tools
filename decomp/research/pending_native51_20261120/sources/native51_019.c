#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
extern s32 D_8015C5FC;
extern u8 D_801C7743;
extern s32 D_801C7750_1C8350;

void func_802220E0_5DD5B0(void) {
    if (D_8015C5FC < (s32) D_801C7743) {
        D_801C7750_1C8350 = 0;
        return;
    }
    if (D_8015C5FC == D_801C7743) {
        D_801C7750_1C8350 = 1;
        return;
    }
    D_801C7750_1C8350 = 2;
}
