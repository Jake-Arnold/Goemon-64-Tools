typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef short s16;typedef unsigned int u32;typedef int s32;typedef float f32;typedef double f64;typedef unsigned long long u64;typedef long long s64;
#include "m2c_macros.h"
s32 func_800236E4_242E4(void *, M2C_UNK);                   /* extern */

s32 func_801D23BC_66490C(void *arg0) {
    if (func_800236E4_242E4(arg0, 0x304) == M2C_FIELD(arg0, s32 *, -4)) {
        return 1;
    }
    return 0;
}
