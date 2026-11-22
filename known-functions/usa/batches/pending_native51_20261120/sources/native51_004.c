#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
M2C_UNK func_801DACDC_596BEC(s32, M2C_UNK);         /* extern */
M2C_UNK func_801E62D0_5A21E0();                     /* extern */

void func_801E01A0_59C0B0(s32 arg0, void *arg1) {
    if ((f64) M2C_FIELD(arg1, f32 *, 0x28) <= 0.0) {
        func_801E62D0_5A21E0();
        func_801DACDC_596BEC(arg0, 0);
    }
}
