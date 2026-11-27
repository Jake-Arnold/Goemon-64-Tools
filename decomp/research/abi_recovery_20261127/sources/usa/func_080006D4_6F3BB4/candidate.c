#include "m2c_types.h"
extern char func_80034ED4_35AD4;
extern char func_8021804C_5D351C;

void func_080006D4_6F3BB4(void *arg0, M2C_UNK arg1) {
    void *temp_v0;

    ((M2C_UNK  (*)(void *, M2C_UNK))&func_8021804C_5D351C)(arg0, 0);
    temp_v0 = M2C_FIELD(arg0, void **, 0xDC);
    if (temp_v0 != NULL) {
        M2C_FIELD(temp_v0, s8 *, 0xD0) = 1;
    }
    ((M2C_UNK (*)())&func_80034ED4_35AD4)();
}
