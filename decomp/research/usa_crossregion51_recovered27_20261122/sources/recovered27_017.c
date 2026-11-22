typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef short s16;typedef unsigned int u32;typedef int s32;typedef float f32;typedef double f64;typedef unsigned long long u64;typedef long long s64;
#include "m2c_macros.h"
M2C_UNK func_801E84A4_5A43B4(void *);               /* extern */
M2C_UNK func_801E1150_59D060(void *);                     /* static */

void func_801E1030_59CF40(void *arg0, M2C_UNK arg1) {
    u8 temp_v0;

    func_801E1150_59D060(arg0);
    temp_v0 = M2C_FIELD(arg0, u8 *, 0x60);
    if ((temp_v0 == 1) || (temp_v0 == 2)) {
        func_801E84A4_5A43B4(arg0);
    }
}
