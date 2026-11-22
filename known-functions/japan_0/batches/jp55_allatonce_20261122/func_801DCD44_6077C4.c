typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef short s16;typedef unsigned int u32;typedef int s32;typedef float f32;typedef double f64;typedef unsigned long long u64;typedef long long s64;
#include "m2c_macros.h"
M2C_UNK func_80034B44_35744(void *);                /* extern */
M2C_UNK func_801DB75C_6061DC();                     /* static */

void func_801DCD44_6077C4(void *arg0, M2C_UNK arg1) {
    s32 temp_t7;

    func_801DB75C_6061DC();
    temp_t7 = --M2C_FIELD(arg0, s32 *, 0x7C);
    if (temp_t7 == 0) {
        func_80034B44_35744(arg0);
    }
}
