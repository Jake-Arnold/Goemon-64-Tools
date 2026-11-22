#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
s32 func_801E0158_59C068(void *arg0) {
    void *temp_v0;
    void *temp_v1;

    if (M2C_FIELD(arg0, u8 *, 0x60) == 0) {
        temp_v1 = M2C_FIELD(arg0, void **, 0x5C);
        temp_v0 = M2C_FIELD(temp_v1, void **, 0x90);
        if ((temp_v0 != NULL) && (M2C_FIELD(temp_v0, u16 *, 0x5C) == 0x245)) {
            return M2C_FIELD(temp_v1, u16 *, 0x86) == 0;
        }
    }
    return 0;
}
