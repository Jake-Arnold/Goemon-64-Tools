#include "m2c_types.h"
extern char func_8003521C_35E1C;
M2C_UNK func_080042FC_6DE1CC();                     /* static */

void func_0800429C_6DE16C(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        if (M2C_FIELD(arg0, u16 *, 0xDE) == M2C_FIELD(arg0, s32 *, 0xD0)) {
            M2C_FIELD(arg0, u16 *, 0xDE) = 0U;
            M2C_FIELD(arg0, u16 *, 0xDC) = (u16) ((M2C_FIELD(arg0, u16 *, 0xDC) + 0x200) & 0x3FF);
        }
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080042FC_6DE1CC);
    }
}
