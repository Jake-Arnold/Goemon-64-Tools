typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef short s16;typedef unsigned int u32;typedef int s32;typedef float f32;typedef double f64;typedef unsigned long long u64;typedef long long s64;
#include "m2c_macros.h"
M2C_UNK func_801DB86C_6062EC();                     /* extern */
M2C_UNK func_80205DB4_630834(void *);               /* static */
M2C_UNK func_802097AC_63422C(void *);               /* static */
extern void *func_80214670_5CFC00;

void func_80206AA4_631524(void *arg0, M2C_UNK arg1) {
    s32 temp_t8;

    M2C_FIELD(func_80214670_5CFC00, s8 *, 7) = 0;
    func_801DB86C_6062EC();
    temp_t8 = --M2C_FIELD(arg0, s32 *, 0x7C);
    if (temp_t8 == 0) {
        func_80205DB4_630834(arg0);
        return;
    }
    func_802097AC_63422C(arg0);
}
