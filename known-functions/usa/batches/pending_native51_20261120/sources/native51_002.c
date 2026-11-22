#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
extern M2C_UNK D_8015C5D8_15D1D8;

s32 func_801DCCF0_598C00(s16 arg0) {
    M2C_FIELD(&D_8015C5D8_15D1D8, s32 *, 0x10) = (s32) (M2C_FIELD(&D_8015C5D8_15D1D8, s32 *, 0x10) + arg0);
    if (M2C_FIELD(&D_8015C5D8_15D1D8, s16 *, 0x12) < 0) {
        M2C_FIELD(&D_8015C5D8_15D1D8, s32 *, 0x10) = 0;
        return 1;
    }
    if (M2C_FIELD(&D_8015C5D8_15D1D8, s16 *, 0x12) >= 0x2710) {
        M2C_FIELD(&D_8015C5D8_15D1D8, s32 *, 0x10) = 0x270F;
        return 1;
    }
    return 0;
}
