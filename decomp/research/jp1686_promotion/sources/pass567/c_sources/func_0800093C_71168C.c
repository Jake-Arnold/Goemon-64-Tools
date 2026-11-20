#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08000978_7116C8();                     /* static */

void func_0800093C_71168C(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, s32 *, 0x68) & 1) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000978_7116C8);
    }
}
