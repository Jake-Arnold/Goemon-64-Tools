#include "m2c_types.h"
M2C_UNK func_80034ED4_35AD4(void);
M2C_UNK func_8021804C_5D351C(void *, s32);

void func_08002AD8_728F68(void *arg0, M2C_UNK arg1) {
    void *temp_v0;

    ((void (*)(void *, s32))func_8021804C_5D351C)(arg0, 0);
    temp_v0 = M2C_FIELD(arg0, void **, 0xDC);
    if (temp_v0 != NULL) {
        M2C_FIELD(temp_v0, s8 *, 0xD0) = 1;
    }
    ((void (*)(void))func_80034ED4_35AD4)();
}
