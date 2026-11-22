typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef short s16;typedef unsigned int u32;typedef int s32;typedef float f32;typedef double f64;typedef unsigned long long u64;typedef long long s64;
#include "m2c_macros.h"
s32 func_801D2C88_58EB98(void *);                         /* static */
M2C_UNK func_801D2E10_58ED20(void *, s32, M2C_UNK, s32); /* static */

void func_801D2BF8_58EB08(void *arg0, s32 arg1) {
    if (func_801D2C88_58EB98(arg0) == 0) {
        func_801D2E10_58ED20(arg0, arg1, 0, ((M2C_FIELD(arg0, u8 *, 0xBC) & 7) << 7) & 0xFFFF);
    }
}
