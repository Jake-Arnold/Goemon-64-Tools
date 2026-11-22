typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef short s16;typedef unsigned int u32;typedef int s32;typedef float f32;typedef double f64;typedef unsigned long long u64;typedef long long s64;
#include "m2c_macros.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_8020D3F4_637E74();                     /* static */

void func_8020D3BC_637E3C(void *arg0, M2C_UNK arg1) {
    s32 temp_t7;

    temp_t7 = --M2C_FIELD(arg0, s32 *, 0x7C);
    if (temp_t7 == 0) {
        func_80034E8C_35A8C(func_8020D3F4_637E74);
    }
}
