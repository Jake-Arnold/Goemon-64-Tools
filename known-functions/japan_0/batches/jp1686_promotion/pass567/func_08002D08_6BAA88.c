#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08002D44_6BAAC4();                     /* static */

void func_08002D08_6BAA88(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s16 *, 0x8A) = 0x3C;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08002D44_6BAAC4);
}
