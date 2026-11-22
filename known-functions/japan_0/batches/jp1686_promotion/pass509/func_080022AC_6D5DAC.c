#include "m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_080022EC_6D5DEC();                     /* static */

void func_080022AC_6D5DAC(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080022EC_6D5DEC);
    }
}
