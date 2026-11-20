#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801D2EE4_5FE2C4(s32, M2C_UNK *);       /* extern */
M2C_UNK func_801F7074_622454();                     /* extern */
M2C_UNK func_801F76D0_622AB0(s32);                  /* extern */
extern M2C_UNK D_8020B2C8_6366A8;
extern M2C_UNK func_801F4654_61FA34;

void func_801F45A0_61F980(s32 arg0, s32 arg1) {
    func_801F7074_622454();
    func_801F76D0_622AB0(arg0);
    func_801D2EE4_5FE2C4(arg1, &D_8020B2C8_6366A8);
    func_8003521C_35E1C(&func_801F4654_61FA34);
}
