#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08008860_6C05E0();                     /* static */

void func_08008824_6C05A4(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s8 *, 0xDD) = 0x38;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08008860_6C05E0);
}
