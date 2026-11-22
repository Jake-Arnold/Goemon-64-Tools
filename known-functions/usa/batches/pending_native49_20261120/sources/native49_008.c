#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
s32 func_801F3AF0_5AFA00(void *arg0) {
    s32 var_v1;
    void *var_v0;

    var_v0 = M2C_FIELD(arg0, void **, 0);
    var_v1 = 0;
    if (var_v0 != NULL) {
loop_2:
        if ((s32) M2C_FIELD(arg0, u16 *, 0x20) < (s32) M2C_FIELD(var_v0, u16 *, 0x20)) {
            var_v0 = M2C_FIELD(var_v0, void **, 0);
            var_v1 += 1;
            if (var_v0 != NULL) {
                goto loop_2;
            }
        }
    }
    return var_v1;
}
