#include "m2c_types.h"
void func_80034B44_35744(void);

void func_080036B0_708D50(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, u16 *, 0x8A)-- == 0) {
        ((void (*)(void))(u32)func_80034B44_35744)();
    }

    *(volatile s32 *)0x80000000 = 1;
}
