#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
extern f64 D_80217BB8_676B68;
extern f64 D_80217BC0_676B70;

void func_80215A10_6749C0(s32 arg0, f32 *arg1, f32 *arg2, f32 *arg3) {
    f64 temp_f0;

    temp_f0 = (f64) arg0 + 0.5;
    *arg1 = (f32) (15.0 - (temp_f0 * 10.0));
    *arg2 = (f32) (temp_f0 * D_80217BB8_676B68);
    *arg3 = (f32) (temp_f0 * D_80217BC0_676B70);
}
