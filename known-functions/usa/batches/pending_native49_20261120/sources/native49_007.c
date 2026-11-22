#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
void func_801E8E8C_5A4D9C(void *arg0) {
    void *var_v0;

    if (arg0 != NULL) {
        var_v0 = M2C_FIELD(arg0, void **, 0x18);
        if (var_v0 != NULL) {
            do {
                M2C_FIELD(var_v0, s8 *, 0x64) = 1;
                M2C_FIELD(var_v0, s32 *, 0x2C) = 0;
                M2C_FIELD(var_v0, s32 *, 0x30) = 0;
                var_v0 = M2C_FIELD(var_v0, void **, 0);
            } while (var_v0 != NULL);
        }
    }
}
