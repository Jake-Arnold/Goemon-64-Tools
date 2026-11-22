#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
s32 func_80014840_15440();                          /* extern */

s32 func_80225E20_5E12F0(s32 arg0, s32 arg1) {
    s32 var_v1;

    if (arg1 != 0) {
        var_v1 = func_80014840_15440();
    } else {
        var_v1 = arg0;
    }
    return var_v1;
}
