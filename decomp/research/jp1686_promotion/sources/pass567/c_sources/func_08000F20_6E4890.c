#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08000F5C_6E48CC();                     /* static */

void func_08000F20_6E4890(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s16 *, 0x8A) = 0x8C;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000F5C_6E48CC);
}
