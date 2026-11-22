#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
s32 func_80034DD8_359D8(M2C_UNK *, M2C_UNK);        /* extern */
M2C_UNK func_801F9230_5B5140();                     /* extern */
extern s16 D_8006D324_6DF24;
extern s32 D_8015C578_15D178;
extern M2C_UNK func_80020724_21324;

void func_801F91F0_5B5100(void) {
    D_8006D324_6DF24 = 0x42;
    D_8015C578_15D178 = func_80034DD8_359D8(&func_80020724_21324, 0);
    func_801F9230_5B5140();
}
