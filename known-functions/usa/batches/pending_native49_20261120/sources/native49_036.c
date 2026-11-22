#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
void func_080003B0_6BFB00(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, s32 *, 0x68) & 0x20000) {
        if (M2C_FIELD(arg0, s32 *, 0xD0) == 1) {
            M2C_FIELD(arg0, s32 *, 0x60) = 0;
            return;
        }
        M2C_FIELD(arg0, s32 *, 0x60) = 0x20;
        return;
    }
    if (M2C_FIELD(arg0, s32 *, 0xD0) == 1) {
        M2C_FIELD(arg0, s32 *, 0x60) = 0x80000000;
        return;
    }
    M2C_FIELD(arg0, s32 *, 0x60) = 0x80000020;
}
