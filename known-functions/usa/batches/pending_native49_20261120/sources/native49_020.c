#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
void func_8021A510_683EF0(void *arg0, void *arg1) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), void **, 0x18);
    if (temp_v0 != NULL) {
        M2C_FIELD(arg1, f32 *, 8) = (f32) M2C_FIELD(temp_v0, f32 *, 8);
        M2C_FIELD(arg1, f32 *, 0xC) = (f32) M2C_FIELD(temp_v0, f32 *, 0xC);
        M2C_FIELD(arg1, f32 *, 0x10) = (f32) M2C_FIELD(temp_v0, f32 *, 0x10);
        M2C_FIELD(arg1, u16 *, 0x14) = (u16) M2C_FIELD(temp_v0, u16 *, 0x14);
        M2C_FIELD(arg1, u16 *, 0x16) = (u16) M2C_FIELD(temp_v0, u16 *, 0x16);
        M2C_FIELD(arg1, u16 *, 0x18) = (u16) M2C_FIELD(temp_v0, u16 *, 0x18);
        M2C_FIELD(arg1, f32 *, 0x1C) = (f32) M2C_FIELD(temp_v0, f32 *, 0x1C);
        M2C_FIELD(arg1, f32 *, 0x20) = (f32) M2C_FIELD(temp_v0, f32 *, 0x20);
        M2C_FIELD(arg1, f32 *, 0x24) = (f32) M2C_FIELD(temp_v0, f32 *, 0x24);
        M2C_FIELD(arg1, f32 *, 0x28) = (f32) M2C_FIELD(temp_v0, f32 *, 0x28);
    }
}
