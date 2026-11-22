#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_80200684_62BA64(void *);               /* extern */
M2C_UNK func_8020407C_62F45C(void *);               /* extern */
extern void *D_8020EF40_63A320;
extern M2C_UNK func_802017C8_62CBA8;

void func_80201770_62CB50(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x7C) = 0xC8;
    func_8003521C_35E1C(&func_802017C8_62CBA8);
    if (M2C_FIELD(D_8020EF40_63A320, u8 *, 0xC) != 0) {
        func_80200684_62BA64(arg0);
    }
    func_8020407C_62F45C(arg0);
}
