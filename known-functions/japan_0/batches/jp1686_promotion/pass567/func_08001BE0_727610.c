#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_0800016C_725B9C();                     /* static */
M2C_UNK func_08002944_728374();                     /* static */

void func_08001BE0_727610(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0xC0) = 6;
    M2C_FIELD(arg0, M2C_UNK (**)(), 0xBC) = func_0800016C_725B9C;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08002944_728374);
}
