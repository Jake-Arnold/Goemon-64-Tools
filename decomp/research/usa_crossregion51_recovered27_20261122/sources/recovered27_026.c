typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef short s16;typedef unsigned int u32;typedef int s32;typedef float f32;typedef double f64;typedef unsigned long long u64;typedef long long s64;
#include "m2c_macros.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK (*)());         /* extern */
M2C_UNK func_80207CC4_6330A4();                     /* static */

void func_80207C8C_63306C(void *arg0, M2C_UNK arg1) {
    s32 temp_t7;

    temp_t7 = --M2C_FIELD(arg0, s32 *, 0x7C);
    if (temp_t7 == 0) {
        func_8003521C_35E1C(func_80207CC4_6330A4);
    }
}
