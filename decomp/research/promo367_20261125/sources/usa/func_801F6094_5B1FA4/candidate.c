#include "m2c_types.h"
extern char func_8001B5AC_1C1AC;
M2C_UNK func_801DACDC_596BEC(s32, M2C_UNK);

void func_801F6094_5B1FA4(s32 arg0, void *arg1) {
    if ((((f32(*)())&func_8001B5AC_1C1AC)(arg1) - 1.0f) <= M2C_FIELD(arg1, f32 *, 0x28)) {
        func_801DACDC_596BEC(arg0, 0);
    }
}
