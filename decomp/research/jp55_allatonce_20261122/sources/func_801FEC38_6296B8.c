typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef short s16;typedef unsigned int u32;typedef int s32;typedef float f32;typedef double f64;typedef unsigned long long u64;typedef long long s64;
#include "m2c_macros.h"
M2C_UNK func_80034B44_35744();                      /* extern */
extern void *D_80214600_63F080;

void func_801FEC38_6296B8(void *arg0, M2C_UNK arg1) {
    s32 temp_t0;

    if (M2C_FIELD(M2C_FIELD(D_80214600_63F080, void **, 0x1D8), s32 *, 0xD8) != 0x16) {
        func_80034B44_35744();
        return;
    }
    temp_t0 = --M2C_FIELD(arg0, s32 *, 0x7C);
    if (temp_t0 == 0) {
        M2C_FIELD(arg0, s16 *, 0x5C) = 0;
        func_80034B44_35744();
    }
}
