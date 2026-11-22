#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021DFEC_5D957C;
M2C_UNK func_08001844_718CE4();                     /* static */

void func_080017F8_718C98(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_8021DFEC_5D957C)();
    M2C_FIELD(arg0, s16 *, 0x8A) = 0x12C;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001844_718CE4);
}
