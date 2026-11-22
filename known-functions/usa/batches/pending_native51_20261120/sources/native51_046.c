#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
extern f64 D_80217740_6766F0;
extern f64 D_80217748_6766F8;

void func_8020FE60_66EE10(void *arg0, f32 arg1) {
    f32 temp_f0;
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    if (temp_v0 != NULL) {
        temp_f0 = (f32) ((f64) arg1 * D_80217740_6766F0);
        M2C_FIELD(temp_v0, f32 *, 0x1C) = temp_f0;
        M2C_FIELD(temp_v0, f32 *, 0x20) = temp_f0;
        M2C_FIELD(temp_v0, f32 *, 0x24) = temp_f0;
    }
    M2C_FIELD(arg0, f32 *, 0x6C) = (f32) ((f64) arg1 * D_80217748_6766F8);
}
