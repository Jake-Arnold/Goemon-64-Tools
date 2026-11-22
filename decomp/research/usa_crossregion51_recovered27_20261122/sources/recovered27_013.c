typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef short s16;typedef unsigned int u32;typedef int s32;typedef float f32;typedef double f64;typedef unsigned long long u64;typedef long long s64;
#include "m2c_macros.h"
M2C_UNK func_80024734_25334(s32);                   /* extern */
M2C_UNK func_80034ED4_35AD4();                      /* extern */

void func_80024848_25448(void *arg0, M2C_UNK arg1) {
    s32 temp_t7;

    temp_t7 = --M2C_FIELD(arg0, s32 *, 0xDC);
    if (temp_t7 == 0) {
        func_80024734_25334(M2C_FIELD(arg0, s32 *, 0xD0));
        func_80034ED4_35AD4();
    }
}
