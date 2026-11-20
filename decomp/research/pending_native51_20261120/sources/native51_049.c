#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
f32 func_8001B5AC_1C1AC(void *);                    /* extern */

void func_80213100_67CAE0(void *arg0, void *arg1) {
    if (M2C_FIELD(arg0, u8 *, 0x5C) == 0) {
        M2C_FIELD(arg1, s16 *, 0x16) = 0x200;
    }
    M2C_FIELD(arg1, f32 *, 0x28) = (f32) ((f64) M2C_FIELD(arg1, f32 *, 0x28) + 0.25);
    if ((func_8001B5AC_1C1AC(arg1) - 1.0f) < M2C_FIELD(arg1, f32 *, 0x28)) {
        M2C_FIELD(arg1, f32 *, 0x28) = 0.0f;
    }
}
