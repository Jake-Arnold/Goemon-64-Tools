#include "m2c_types.h"
f32 func_8001B5AC_1C1AC(void *);
M2C_UNK func_801DACDC_596BEC(void *, M2C_UNK);

void func_801F7170_5B3080(void *arg0) {
    void *temp_a0;

    temp_a0 = M2C_FIELD(arg0, void **, 0x18);
    if ((((f32 (*)(void *))(s32)func_8001B5AC_1C1AC)(temp_a0) - 1.0f) <= M2C_FIELD(temp_a0, f32 *, 0x28)) {
        func_801DACDC_596BEC(arg0, 0);
    }
}
