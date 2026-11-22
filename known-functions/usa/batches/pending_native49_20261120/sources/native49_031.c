#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
void func_80212A7C_69A47C(void *arg0, f32 arg1, f32 arg2, f32 arg3) {
    f32 temp_f0;
    f32 temp_f0_2;
    f32 temp_f12;
    f32 temp_f12_2;
    f32 temp_f14;
    f32 temp_f14_2;
    f32 var_f2;
    f32 var_f2_2;
    f32 var_f2_3;
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x5C);
    temp_f0 = M2C_FIELD(temp_v0, f32 *, 0x10);
    M2C_FIELD(temp_v0, f32 *, 0x14) = arg1;
    M2C_FIELD(temp_v0, f32 *, 0x20) = arg2;
    M2C_FIELD(temp_v0, f32 *, 0x2C) = arg3;
    if (arg1 < temp_f0) {
        var_f2 = -(M2C_FIELD(temp_v0, f32 *, 0x14) - temp_f0);
    } else {
        var_f2 = M2C_FIELD(temp_v0, f32 *, 0x14) - temp_f0;
    }
    temp_f0_2 = M2C_FIELD(temp_v0, f32 *, 8);
    temp_f12 = M2C_FIELD(temp_v0, f32 *, 0x20);
    temp_f14 = M2C_FIELD(temp_v0, f32 *, 0x1C);
    M2C_FIELD(temp_v0, f32 *, 0x18) = (f32) (var_f2 / temp_f0_2);
    if (temp_f12 < temp_f14) {
        var_f2_2 = -(temp_f12 - temp_f14);
    } else {
        var_f2_2 = temp_f12 - temp_f14;
    }
    temp_f12_2 = M2C_FIELD(temp_v0, f32 *, 0x2C);
    temp_f14_2 = M2C_FIELD(temp_v0, f32 *, 0x28);
    M2C_FIELD(temp_v0, f32 *, 0x24) = (f32) (var_f2_2 / temp_f0_2);
    if (temp_f12_2 < temp_f14_2) {
        var_f2_3 = -(temp_f12_2 - temp_f14_2);
    } else {
        var_f2_3 = temp_f12_2 - temp_f14_2;
    }
    M2C_FIELD(temp_v0, f32 *, 0x30) = (f32) (var_f2_3 / temp_f0_2);
}
