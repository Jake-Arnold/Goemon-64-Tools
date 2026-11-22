#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
M2C_UNK func_801DAD08_596C18(s32, M2C_UNK);         /* extern */
M2C_UNK func_801DD720_599630(s32, M2C_UNK);         /* extern */
s32 func_801DF858_59B768(s32);                      /* extern */
s32 func_801DF8B8_59B7C8(s32);                      /* extern */
s32 func_801E1E70_59DD80(s32);                      /* extern */
M2C_UNK func_801E31DC_59F0EC(s32);                  /* extern */
M2C_UNK func_801E7F50_5A3E60();                     /* extern */

void func_801DF6D0_59B5E0(s32 arg0, M2C_UNK arg1) {
    func_801E7F50_5A3E60();
    func_801DD720_599630(arg0, 0xF);
    func_801E31DC_59F0EC(arg0);
    if ((func_801DF858_59B768(arg0) == 0) && (func_801DF8B8_59B7C8(arg0) == 0) && (func_801E1E70_59DD80(arg0) == 0)) {
        func_801DAD08_596C18(arg0, 0x45);
    }
}
