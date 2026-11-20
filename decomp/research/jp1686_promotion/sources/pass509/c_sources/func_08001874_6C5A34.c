#include "m2c_types.h"
extern char func_80023B54_24754;
extern char func_80034E8C_35A8C;
M2C_UNK func_080018C8_6C5A88();                     /* static */

void func_08001874_6C5A34(s32 arg0, void *arg1) {
    M2C_FIELD(arg1, u16 *, 0x16) = (u16) ((M2C_FIELD(arg1, u16 *, 0x16) + 4) & 0x3FF);
    if (((s32(*)())&func_80023B54_24754)(6) != 0) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080018C8_6C5A88);
    }
}
