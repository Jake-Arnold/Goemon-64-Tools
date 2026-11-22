#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_080037EC_6BB56C();                     /* static */

void func_080037B0_6BB530(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080037EC_6BB56C);
}
