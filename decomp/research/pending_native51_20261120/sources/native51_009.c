#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
M2C_UNK func_801DACDC_596BEC(void *, M2C_UNK);      /* extern */
M2C_UNK func_801F7034_5B2F44();                     /* extern */
M2C_UNK func_801F706C_5B2F7C();                     /* extern */

void func_801F6970_5B2880(void *arg0, void *arg1) {
    M2C_FIELD(arg0, u8 *, 0x30) = (u8) (M2C_FIELD(arg0, u8 *, 0x30) & 0xFFFE);
    if (M2C_FIELD(arg1, f32 *, 0x28) <= 0.0f) {
        if (M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u8 *, 0x59) != 0) {
            func_801F7034_5B2F44();
            func_801DACDC_596BEC(arg0, 0x42);
            return;
        }
        func_801F706C_5B2F7C();
        func_801DACDC_596BEC(arg0, 0);
    }
}
