#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
f32 func_801D2F40_5FE320(M2C_UNK, M2C_UNK);         /* extern */
M2C_UNK func_801D60E4_6014C4(s32);                  /* extern */
M2C_UNK func_801F0540_61B920(s32);                  /* extern */
s32 func_801F732C_62270C(s32);                      /* extern */
M2C_UNK func_801F76D0_622AB0(s32);                  /* extern */

void func_801F2FA0_61E380(s32 arg0, M2C_UNK arg1) {
    f32 sp1C;

    sp1C = func_801D2F40_5FE320(arg1, 0x42480000);
    func_801F76D0_622AB0(arg0);
    func_801D60E4_6014C4(arg0);
    if ((func_801F732C_62270C(arg0) != 0) && (sp1C == 0.0f)) {
        func_801F0540_61B920(arg0);
    }
}
