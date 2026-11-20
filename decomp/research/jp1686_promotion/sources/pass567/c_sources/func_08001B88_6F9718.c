#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08001BC4_6F9754();                     /* static */

void func_08001B88_6F9718(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s16 *, 0x8A) = 0x14;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001BC4_6F9754);
}
