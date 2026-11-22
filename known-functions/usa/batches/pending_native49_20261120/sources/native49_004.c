#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
void func_801E54A8_5A13B8(void *arg0, void *arg1) {
    void *temp_v0;

    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), void **, 0x8C) = arg1;
    temp_v0 = M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), void **, 0x8C);
    if (temp_v0 != NULL) {
        M2C_FIELD(temp_v0, s32 *, 0x68) = (s32) (M2C_FIELD(temp_v0, s32 *, 0x68) | 0x8000);
        M2C_FIELD(arg0, f32 *, 0xE8) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0xE4) = 0.0f;
    }
}
