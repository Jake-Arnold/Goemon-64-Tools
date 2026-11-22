#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_0800193C_6E52AC();                     /* static */

void func_08001900_6E5270(s32 arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_0800193C_6E52AC);
    }
}
