#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
M2C_UNK func_801D6934_645784();                     /* extern */

void func_801D61D0_645020(void *arg0) {
    s32 temp_v1;
    s32 var_v0;

    temp_v1 = M2C_FIELD(arg0, s32 *, 0xB4);
    var_v0 = M2C_FIELD(arg0, s32 *, 0xB0) + temp_v1;
    if ((var_v0 == 0) || ((var_v0 ^ temp_v1) >= 0)) {
        M2C_FIELD(arg0, s8 *, 0xA1) = 3;
        var_v0 = 0;
    }
    M2C_FIELD(arg0, s32 *, 0xB0) = var_v0;
    func_801D6934_645784();
}
