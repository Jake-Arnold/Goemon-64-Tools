#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
f32 func_801D2F40_5FE320(s32, M2C_UNK);             /* extern */
M2C_UNK func_801F1394_61C774(s32, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801F76D0_622AB0();                     /* extern */

void func_801F1340_61C720(s32 arg0, s32 arg1) {
    func_801F76D0_622AB0();
    if (func_801D2F40_5FE320(arg1, 0x42480000) == 0.0f) {
        func_801F1394_61C774(arg0, 0x64, 0x41000000);
    }
}
