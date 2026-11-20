#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
M2C_UNK func_801D4BF4_5FFFD4(s32, M2C_UNK);         /* extern */
M2C_UNK func_80200684_62BA64(s32);                  /* extern */
M2C_UNK func_8020407C_62F45C(s32);                  /* extern */
M2C_UNK func_80204624_62FA04();                     /* extern */
extern s32 D_8020EED0_63A2B0;
extern void *D_8020EF40_63A320;

void func_80200760_62BB40(s32 arg0, s32 arg1) {
    void *sp1C;

    sp1C = D_8020EED0_63A2B0 + 0x140;
    func_80204624_62FA04();
    func_801D4BF4_5FFFD4(arg1 + 8, 0x3F800000);
    if (M2C_FIELD(sp1C, u8 *, 0xE) != 5) {
        M2C_FIELD(D_8020EF40_63A320, s8 *, 4) = 0;
        func_80200684_62BA64(arg0);
    }
    func_8020407C_62F45C(arg0);
}
