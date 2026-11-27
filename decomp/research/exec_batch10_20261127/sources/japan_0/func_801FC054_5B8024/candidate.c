#include "m2c_types.h"
f32 func_8001B13C_1BD3C(void *);
M2C_UNK func_801E019C_59C16C(void *, M2C_UNK);

void func_801FC054_5B8024(void *arg0) {
    void *temp_a0;

    temp_a0 = M2C_FIELD(arg0, void **, 0x18);
    if ((((f32 (*)(void *))(s32)func_8001B13C_1BD3C)(temp_a0) - 1.0f) <= M2C_FIELD(temp_a0, f32 *, 0x28)) {
        func_801E019C_59C16C(arg0, 0);
    }
}
