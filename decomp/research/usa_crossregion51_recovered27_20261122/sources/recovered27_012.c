typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef short s16;typedef unsigned int u32;typedef int s32;typedef float f32;typedef double f64;typedef unsigned long long u64;typedef long long s64;
#include "m2c_macros.h"
void func_080017CC_6EA91C(void *arg0, void *arg1) {
    s32 temp_t2;
    u16 temp_v0;

    temp_v0 = M2C_FIELD(arg1, u16 *, 0x16);
    M2C_FIELD(arg1, u16 *, 0x14) = (u16) M2C_FIELD(M2C_FIELD(M2C_FIELD(arg0, void **, 0xE8), void **, 0x18), u16 *, 0x14);
    temp_t2 = (M2C_FIELD(M2C_FIELD(M2C_FIELD(arg0, void **, 0xD0), void **, 0x18), u16 *, 0x16) - temp_v0) & 0x3FF;
    if ((temp_t2 >= 0x50) && (temp_t2 < 0x3B1)) {
        M2C_FIELD(arg1, u16 *, 0x16) = (u16) (temp_v0 += M2C_FIELD(arg0, u16 *, 0xE4));
    }
}
