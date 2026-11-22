#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
extern M2C_UNK D_800C4CC0;
extern s8 D_800C7AE2;
extern s8 D_8015C562_15D162;
extern void *D_801FC604_5B8514;

void func_80221F70_5DD440(void) {
    D_800C7AE2 = 1;
    *M2C_FIELD(D_801FC604_5B8514, s16 **, 0x5C) = 0;
    M2C_FIELD(&D_800C4CC0, s16 *, 0x30F4) = 0;
    M2C_FIELD(&D_800C4CC0, s16 *, 0x30F2) = 0;
    M2C_FIELD(&D_800C4CC0, s16 *, 0x30F6) = 0;
    M2C_FIELD(&D_800C4CC0, s16 *, 0x30F8) = 0;
    D_8015C562_15D162 = 1;
}
