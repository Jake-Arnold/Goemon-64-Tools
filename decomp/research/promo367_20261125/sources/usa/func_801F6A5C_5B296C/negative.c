#include "m2c_types.h"
extern char func_8001B5AC_1C1AC;
M2C_UNK func_801DACDC_596BEC(void *, M2C_UNK);
M2C_UNK func_801E7F50_5A3E60();

void func_801F6A5C_5B296C(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    func_801E7F50_5A3E60();
    if ((((f32(*)())&func_8001B5AC_1C1AC)(arg1) - 1.0f) <= M2C_FIELD(arg1, f32 *, 0x28)) {
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), f32 *, 0xAC) = 3.0f;
        func_801DACDC_596BEC(arg0, 0xB0);
    }
}
