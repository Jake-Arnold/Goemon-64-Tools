#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
M2C_UNK func_801FFE14_62B1F4();                     /* extern */
M2C_UNK func_801FFE6C_62B24C();                     /* extern */
extern void *D_8020EF40_63A320;

void func_801FB6A0_626A80(void *arg0, M2C_UNK arg1) {
    func_801FFE6C_62B24C();
    M2C_FIELD(D_8020EF40_63A320, s8 *, 0x815) = 0;
    func_801FFE14_62B1F4();
    M2C_FIELD(arg0, s16 *, 0x5C) = 0x82;
    M2C_FIELD(arg0, s32 *, 0x7C) = 0xC8;
}
