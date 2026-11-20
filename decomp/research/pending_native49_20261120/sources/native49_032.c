#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
void func_80212B40_69A540(void *arg0, f32 arg1) {
    f32 temp_f0;
    f32 var_f2;
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x5C);
    M2C_FIELD(temp_v0, f32 *, 0x4C) = arg1;
    temp_f0 = M2C_FIELD(M2C_FIELD(temp_v0, void **, 0x54), f32 *, 0x24);
    if (arg1 < temp_f0) {
        var_f2 = -(M2C_FIELD(temp_v0, f32 *, 0x4C) - temp_f0);
    } else {
        var_f2 = M2C_FIELD(temp_v0, f32 *, 0x4C) - temp_f0;
    }
    M2C_FIELD(temp_v0, f32 *, 0x50) = (f32) (var_f2 / M2C_FIELD(temp_v0, f32 *, 8));
}
