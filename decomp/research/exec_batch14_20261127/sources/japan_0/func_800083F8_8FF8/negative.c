#include "m2c_types.h"

void func_800083A4_8FA4(u8, u8, u8, u8);

void func_800083F8_8FF8(u8 arg0, u8 *arg1) {
    u8 i;

    for (i = 0; i < 0x10; i++) {
        func_800083A4_8FA4(arg0, arg1[0], arg1[i + 1], i);
    }

    *(volatile int *)0x80000000 = 1;
}
