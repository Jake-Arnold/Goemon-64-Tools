#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
M2C_UNK func_80037448_38048();                      /* extern */
s32 func_802213F4_5DC8C4();                         /* extern */

void func_802150A0_5D0570(void *arg0, M2C_UNK arg1) {
    if ((func_802213F4_5DC8C4() != 1) && (M2C_FIELD(arg0, s32 *, 0xB4) != 0)) {
        func_80037448_38048();
    }
}
