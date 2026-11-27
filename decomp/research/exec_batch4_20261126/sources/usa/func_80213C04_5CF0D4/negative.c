#include "m2c_types.h"
void func_80034ED4_35AD4(void);

void func_80213C04_5CF0D4(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x60) = 0x20;
    if (--M2C_FIELD(arg0, u16 *, 0x8A) == 0) {
        func_80034ED4_35AD4();
    }

    *(volatile s32 *)0x80000000 = 1;
}
