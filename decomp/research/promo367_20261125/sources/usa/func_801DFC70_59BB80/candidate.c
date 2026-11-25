#include "m2c_types.h"
extern char func_8001B5AC_1C1AC;
M2C_UNK func_801DACDC_596BEC(void *, M2C_UNK);

void func_801DFC70_59BB80(void *arg0, void *arg1) {
    if ((((f32(*)())&func_8001B5AC_1C1AC)(arg1) - 1.0f) <= M2C_FIELD(arg1, f32 *, 0x28)) {
        *M2C_FIELD(arg0, s16 **, 0x5C) = 0;
        func_801DACDC_596BEC(arg0, 0);
    }
}
