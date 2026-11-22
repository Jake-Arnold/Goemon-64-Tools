#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801D2EE4_5FE2C4(s32, M2C_UNK *);       /* extern */
M2C_UNK func_801FFE34_62B214();                     /* extern */
M2C_UNK func_801FFE6C_62B24C();                     /* extern */
extern M2C_UNK D_8020B430_636810;
extern void *D_8020EF40_63A320;
extern M2C_UNK func_801FF798_62AB78;

void func_801FF730_62AB10(void *arg0, s32 arg1) {
    func_801FFE6C_62B24C();
    func_801FFE34_62B214();
    func_801D2EE4_5FE2C4(arg1, &D_8020B430_636810);
    M2C_FIELD(D_8020EF40_63A320, s8 *, 0x816) = 2;
    M2C_FIELD(arg0, s32 *, 0xEC) = (s32) (M2C_FIELD(arg0, s32 *, 0xEC) + 1);
    func_8003521C_35E1C(&func_801FF798_62AB78);
}
