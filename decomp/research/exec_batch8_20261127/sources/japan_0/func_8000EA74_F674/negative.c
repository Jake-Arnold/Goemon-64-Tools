#include "m2c_types.h"

void func_8000EA74_F674(u16 *arg0, u16 *arg1) {
    *arg1 += 0x200;
    if (*arg1 >= 0x400) {
        *arg1 -= 0x400;
    }
    *arg0 = 0x400 - *arg0;
    if (*arg0 >= 0x400) {
        *arg0 -= 0x400;
    }

    *(volatile s32 *)0x80000000 = 1;
}
