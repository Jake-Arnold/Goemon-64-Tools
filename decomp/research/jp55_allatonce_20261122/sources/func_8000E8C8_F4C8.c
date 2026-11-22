typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef short s16;typedef unsigned int u32;typedef int s32;typedef float f32;typedef double f64;typedef unsigned long long u64;typedef long long s64;
#include "m2c_macros.h"
s32 func_80003FD8_4BD8(f32, f32);                   /* extern */

u16 func_8000E8C8_F4C8(f32 arg0, f32 arg1, f32 arg2, f32 arg3) {
    return func_80003FD8_4BD8(arg0 - arg2, arg1 - arg3) & 0x3FF;
}
