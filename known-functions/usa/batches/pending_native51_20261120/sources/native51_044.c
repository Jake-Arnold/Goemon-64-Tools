#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
M2C_UNK func_801D0910_63F760();                     /* extern */
M2C_UNK func_801D0960_63F7B0();                     /* extern */
M2C_UNK func_801D09AC_63F7FC();                     /* extern */
M2C_UNK func_801D09F8_63F848();                     /* extern */

void func_801D0850_63F6A0(void *arg0) {
    s32 temp_v0_2;
    s8 temp_v0;

    temp_v0 = M2C_FIELD(arg0, s8 *, 0x9F);
    if (temp_v0 & 1) {
        M2C_FIELD(arg0, s8 *, 0x9F) = (s8) (temp_v0 & 0xFFFE);
        M2C_FIELD(arg0, s32 *, 0xB0) = 0;
    }
    M2C_FIELD(arg0, s8 *, 0xA2) = 0x14;
    if (M2C_FIELD(arg0, u8 *, 0x9E) == 0) {
        M2C_FIELD(arg0, s8 *, 0x9D) = 1;
        func_801D0910_63F760();
        if (M2C_FIELD(arg0, s8 *, 0xC4) != 0) {
            M2C_FIELD(arg0, s8 *, 0xC4) = 0;
            M2C_FIELD(arg0, s32 *, 0xB4) = 0x2710;
        }
    } else {
        temp_v0_2 = M2C_FIELD(arg0, s32 *, 0xB4);
        if (temp_v0_2 < 0x3A99) {
            M2C_FIELD(arg0, s8 *, 0x9D) = 2;
            func_801D0960_63F7B0();
            return;
        }
        if (temp_v0_2 < 0x4651) {
            M2C_FIELD(arg0, s8 *, 0x9D) = 3;
            func_801D09AC_63F7FC();
            return;
        }
        M2C_FIELD(arg0, s8 *, 0x9D) = 4;
        func_801D09F8_63F848();
    }
}
