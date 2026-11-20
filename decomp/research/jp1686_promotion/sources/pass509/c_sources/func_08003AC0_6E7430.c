#include "m2c_types.h"
extern char func_8021DFEC_5D957C;
extern char func_8021FE0C_5DB39C;

void func_08003AC0_6E7430(void *arg0, M2C_UNK arg1) {
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        ((M2C_UNK(*)())&func_8021DFEC_5D957C)();
        ((M2C_UNK(*)())&func_8021FE0C_5DB39C)(arg0, 0, 1);
    }
}
