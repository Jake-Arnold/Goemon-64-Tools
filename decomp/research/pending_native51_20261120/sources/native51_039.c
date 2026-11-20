#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
M2C_UNK func_801D3018_5FE3F8(M2C_UNK, M2C_UNK);     /* extern */
M2C_UNK func_801FC3FC_6277DC(void *);               /* extern */
extern s32 D_8020EED0_63A2B0;
extern void *D_8020EF40_63A320;

void func_801FFA40_62AE20(void *arg0, M2C_UNK arg1) {
    void *sp1C;

    sp1C = D_8020EED0_63A2B0 + 0x140;
    M2C_FIELD(D_8020EF40_63A320, s8 *, 0x816) = 2;
    func_801D3018_5FE3F8(arg1, 0x42700000);
    if (M2C_FIELD(sp1C, u8 *, 0xE) == 3) {
        M2C_FIELD(arg0, s32 *, 0xD4) = 0xA;
        func_801FC3FC_6277DC(arg0);
    }
}
