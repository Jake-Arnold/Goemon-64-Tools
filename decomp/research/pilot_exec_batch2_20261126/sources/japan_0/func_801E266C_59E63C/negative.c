#include "m2c_types.h"
s32 func_801E266C_59E63C(void *arg0) {
    u8 temp_v0;

    if ((M2C_FIELD(arg0, u8 *, 0xEC) != 0) || ((temp_v0 = M2C_FIELD(arg0, u8 *, 0xCC)) >= 0x70 && temp_v0 < 0x7C)) {
        { *(volatile int *)0x80000000 = 1; } return 1;
    }
    return 0;
}
