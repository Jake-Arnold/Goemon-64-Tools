#include "m2c_types.h"

void func_800084F4_90F4(u8, u8, u8, u8);

void func_80008548_9148(u8 arg0, u8 *arg1) {
    u8 i;

    for (i = 0; i < 0x10; i++) {
        func_800084F4_90F4(arg0, arg1[0], arg1[i + 1], i);
    }
}
