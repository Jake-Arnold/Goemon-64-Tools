#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801D2EE4_5FE2C4(s32, M2C_UNK *);       /* extern */
M2C_UNK func_801F7074_622454();                     /* extern */
extern M2C_UNK D_8020B2D0_6366B0;
extern M2C_UNK func_801F4860_61FC40;

void func_801F4780_61FB60(void *arg0, s32 arg1) {
    func_801F7074_622454();
    M2C_FIELD(arg0, f32 *, 0x74) = 7.0f;
    func_801D2EE4_5FE2C4(arg1, &D_8020B2D0_6366B0);
    M2C_FIELD(arg0, s32 *, 0xE8) = (s32) (M2C_FIELD(arg0, s32 *, 0xE8) + 1);
    func_8003521C_35E1C(&func_801F4860_61FC40);
}
