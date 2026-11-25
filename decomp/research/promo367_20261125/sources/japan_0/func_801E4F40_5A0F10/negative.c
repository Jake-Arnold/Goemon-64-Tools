#include "m2c_types.h"
extern char func_8001B13C_1BD3C;
M2C_UNK func_801E019C_59C16C(void *, M2C_UNK);

void func_801E4F40_5A0F10(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    if ((((f32(*)())&func_8001B13C_1BD3C)(arg1) - 1.0f) <= M2C_FIELD(arg1, f32 *, 0x28)) {
        *M2C_FIELD(arg0, s16 **, 0x5C) = 0;
        func_801E019C_59C16C(arg0, 0);
    }
}
