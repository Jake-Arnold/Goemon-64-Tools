#include "m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08004228_6E29B8();                     /* static */

void func_080041C8_6E2958(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        if (M2C_FIELD(arg0, u16 *, 0xDE) == M2C_FIELD(arg0, s32 *, 0xD0)) {
            M2C_FIELD(arg0, u16 *, 0xDE) = 0U;
            M2C_FIELD(arg0, u16 *, 0xDC) = (u16) ((M2C_FIELD(arg0, u16 *, 0xDC) + 0x200) & 0x3FF);
        }
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08004228_6E29B8);
    }
}
