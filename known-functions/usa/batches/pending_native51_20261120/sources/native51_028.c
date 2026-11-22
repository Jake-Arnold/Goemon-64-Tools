#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801D3018_5FE3F8(M2C_UNK, M2C_UNK);     /* extern */
M2C_UNK func_801D31CC_5FE5AC(s32, M2C_UNK *);       /* extern */
M2C_UNK func_801D3F00_5FF2E0(s32, M2C_UNK, M2C_UNK); /* extern */
s32 func_801F732C_62270C(s32);                      /* extern */
M2C_UNK func_801F76D0_622AB0(s32);                  /* extern */
extern M2C_UNK D_8020B2A8_636688;
extern M2C_UNK func_801F0398_61B778;

void func_801F0330_61B710(s32 arg0, M2C_UNK arg1) {
    func_801D3018_5FE3F8(arg1, 0x42200000);
    func_801F76D0_622AB0(arg0);
    func_801D3F00_5FF2E0(arg0, 0, 8);
    if (func_801F732C_62270C(arg0) != 0) {
        func_801D31CC_5FE5AC(arg0, &D_8020B2A8_636688);
        func_8003521C_35E1C(&func_801F0398_61B778);
    }
}
