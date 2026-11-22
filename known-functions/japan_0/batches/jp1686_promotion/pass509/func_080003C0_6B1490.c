#include "m2c_types.h"
extern char func_80034B44_35744;

void func_080003C0_6B1490(void *arg0, M2C_UNK arg1) {
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        ((M2C_UNK(*)())&func_80034B44_35744)();
    }
}
