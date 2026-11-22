#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_8003D310_3DF10(u16);                   /* extern */
extern M2C_UNK func_8022182C_5DCCFC;

void func_80221860_5DCD30(void *arg0, M2C_UNK arg1) {
    func_8003D310_3DF10(M2C_FIELD(arg0, u16 *, 0xA4));
    func_8003521C_35E1C(&func_8022182C_5DCCFC);
}
