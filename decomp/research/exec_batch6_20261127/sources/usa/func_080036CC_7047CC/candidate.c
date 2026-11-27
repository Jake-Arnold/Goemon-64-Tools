#include "m2c_types.h"
void func_80034ED4_35AD4(void);

void func_080036CC_7047CC(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, u16 *, 0x8A)-- == 0) {
        ((void (*)(void))(u32)func_80034ED4_35AD4)();
    }
}
