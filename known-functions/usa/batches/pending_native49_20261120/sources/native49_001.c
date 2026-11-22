#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
void func_80030688_31288(f32 *arg0, f32 *arg1, f32 *arg2, f32 *arg3, void *arg4) {
    f32 temp_f0;
    f32 temp_f0_2;

    temp_f0 = M2C_FIELD(arg4, f32 *, 0x18);
    if (temp_f0 > 0.0f) {
        if (*arg0 < temp_f0) {
            *arg0 = temp_f0;
        }
    } else if (temp_f0 < *arg1) {
        *arg1 = temp_f0;
    }
    temp_f0_2 = M2C_FIELD(arg4, f32 *, 0x20);
    if (temp_f0_2 > 0.0f) {
        if (*arg2 < temp_f0_2) {
            *arg2 = temp_f0_2;
        }
    } else if (temp_f0_2 < *arg3) {
        *arg3 = temp_f0_2;
    }
}
