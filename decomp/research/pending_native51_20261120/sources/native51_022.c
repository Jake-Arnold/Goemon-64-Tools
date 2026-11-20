#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
M2C_UNK func_8000DD58_E958(M2C_UNK);                /* extern */
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
extern void *D_8020EED0_63A2B0;
extern M2C_UNK func_801CBE3C_5F721C;

void func_801CC010_5F73F0(s32 arg0, M2C_UNK arg1) {
    if (M2C_FIELD(D_8020EED0_63A2B0, u8 *, 0x2C4) == 0) {
        func_8003521C_35E1C(&func_801CBE3C_5F721C);
    }
    func_8000DD58_E958(0x11B7);
    M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x2C8) = (s32) (M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x2C8) + 1);
}
