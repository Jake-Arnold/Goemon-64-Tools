#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801FA3FC_5B630C(M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
extern M2C_UNK func_801FA19C_5B60AC;

void func_801FA150_5B6060(s32 arg0, void *arg1) {
    func_801FA3FC_5B630C(0xFF, 0xFF, 0xFF);
    M2C_FIELD(arg1, s8 *, 5) = 0;
    M2C_FIELD(arg1, s16 *, 6) = 1;
    func_8003521C_35E1C(&func_801FA19C_5B60AC);
}
