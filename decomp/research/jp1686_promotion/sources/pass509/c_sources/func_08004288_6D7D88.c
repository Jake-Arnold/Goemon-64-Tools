#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
M2C_UNK func_080042EC_6D7DEC();                     /* static */

void func_08004288_6D7D88(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080042EC_6D7DEC);
        ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 0, 0x3F800000, 1);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x96;
    }
}
