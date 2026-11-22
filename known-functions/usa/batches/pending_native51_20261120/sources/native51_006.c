#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
M2C_UNK func_801E1F5C_59DE6C(s32, M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
s32 func_801E7DE8_5A3CF8();                         /* extern */

void func_801E1E70_59DD80(s32 arg0) {
    if (func_801E7DE8_5A3CF8() != 0) {
        func_801E1F5C_59DE6C(arg0, 0x3F3851EB, 0x3DCCCCCD, 0x41C00000);
        return;
    }
    func_801E1F5C_59DE6C(arg0, 0x3FE66666, 0x3DCCCCCD, 0x41C00000);
}
