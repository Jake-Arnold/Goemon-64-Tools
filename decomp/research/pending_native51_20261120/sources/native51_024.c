#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801D2EE4_5FE2C4(s32, M2C_UNK *);       /* extern */
M2C_UNK func_801D34D0_5FE8B0(s32, M2C_UNK *, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801EF268_61A648();                     /* extern */
extern M2C_UNK D_8020B094_636474;
extern M2C_UNK D_8020B198_636578;
extern M2C_UNK func_801E61A8_611588;

void func_801E6150_611530(s32 arg0, s32 arg1) {
    func_801EF268_61A648();
    func_801D2EE4_5FE2C4(arg1, &D_8020B198_636578);
    func_801D34D0_5FE8B0(arg1, &D_8020B094_636474, 0, 1);
    func_8003521C_35E1C(&func_801E61A8_611588);
}
