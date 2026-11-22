#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
s32 func_801D2C88_58EB98();                         /* extern */
M2C_UNK func_801D2E10_58ED20(void *, s32, u16, s32); /* extern */

void func_801D2C40_58EB50(void *arg0, s32 arg1) {
    if (func_801D2C88_58EB98() == 0) {
        func_801D2E10_58ED20(arg0, arg1, M2C_FIELD(arg0, u16 *, 0xCC), ((M2C_FIELD(arg0, u8 *, 0xBC) & 7) << 7) & 0xFFFF);
    }
}
