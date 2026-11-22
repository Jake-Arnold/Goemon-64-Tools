#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *, void *);     /* extern */
s32 func_80221B7C_5DD04C();                         /* extern */
extern M2C_UNK func_80221338_5DC808;

s32 func_802212F0_5DC7C0(void *arg0) {
    if (func_80221B7C_5DD04C() == 0) {
        return 0;
    }
    M2C_FIELD(arg0, s32 *, 0xB4) = (s32) M2C_FIELD(arg0, s32 *, 0xC);
    func_8003521C_35E1C(&func_80221338_5DC808, arg0);
    return 1;
}
