#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
void func_080013C8_7024C8(void *arg0) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    M2C_FIELD(arg0, f32 *, 0x78) = (f32) M2C_FIELD(temp_v0, f32 *, 8);
    M2C_FIELD(arg0, f32 *, 0x7C) = (f32) M2C_FIELD(temp_v0, f32 *, 0xC);
    M2C_FIELD(arg0, f32 *, 0x80) = (f32) M2C_FIELD(temp_v0, f32 *, 0x10);
    M2C_FIELD(arg0, s16 *, 0xE4) = (s16) (M2C_FIELD(temp_v0, u16 *, 0x14) & 0x3FF);
    M2C_FIELD(arg0, s16 *, 0xE6) = (s16) (M2C_FIELD(temp_v0, u16 *, 0x16) & 0x3FF);
    M2C_FIELD(arg0, s16 *, 0xE8) = (s16) (M2C_FIELD(temp_v0, u16 *, 0x18) & 0x3FF);
}
