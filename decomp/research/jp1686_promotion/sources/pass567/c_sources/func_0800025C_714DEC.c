#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_0800029C_714E2C();                     /* static */
M2C_UNK func_08001100_715C90();                     /* static */

void func_0800025C_714DEC(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, M2C_UNK (**)(), 0xBC) = func_0800029C_714E2C;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001100_715C90);
}
