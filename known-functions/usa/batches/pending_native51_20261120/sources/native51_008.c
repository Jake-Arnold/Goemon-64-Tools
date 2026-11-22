#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
M2C_UNK func_801DCD48_598C58(M2C_UNK, void *);      /* extern */
M2C_UNK func_801E3134_59F044(void *);               /* extern */

void func_801E7F50_5A3E60(void *arg0) {
    void *temp_v0;

    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0x36) = 0;
    temp_v0 = M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), void **, 0x4C);
    if ((temp_v0 != NULL) && (M2C_FIELD(temp_v0, s32 *, 0x64) & 0x100) && (M2C_FIELD(arg0, u8 *, 0xD4) == 0)) {
        func_801DCD48_598C58(-1, arg0);
        func_801E3134_59F044(arg0);
    }
}
