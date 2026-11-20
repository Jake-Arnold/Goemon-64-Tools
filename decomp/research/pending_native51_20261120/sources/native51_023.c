#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
M2C_UNK func_801D614C_60152C();                     /* extern */

s32 func_801D5B70_600F50(void *arg0) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, s32 *, 0x7C);
    if (temp_v0 != 0) {
        M2C_FIELD(arg0, s32 *, 0x7C) = (s32) (temp_v0 - 1);
        func_801D614C_60152C();
        return 0;
    }
    return 1;
}
