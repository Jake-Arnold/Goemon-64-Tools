typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef short s16;typedef unsigned int u32;typedef int s32;typedef float f32;typedef double f64;typedef unsigned long long u64;typedef long long s64;
#include "m2c_macros.h"
s32 func_80023A1C_2461C(void *, M2C_UNK);                   /* extern */

s32 func_801CCCAC_65FB5C(void *arg0) {
    if (func_80023A1C_2461C(arg0, 0x304) == M2C_FIELD(arg0, s32 *, -4)) {
        return 1;
    }
    return 0;
}
