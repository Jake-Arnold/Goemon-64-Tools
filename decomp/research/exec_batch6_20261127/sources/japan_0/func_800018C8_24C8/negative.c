#include "m2c_types.h"
void osWritebackDCache(void *, s32);

void func_800018C8_24C8(u32 *arg0, u32 arg1) {
    arg0[0] = ((arg1 >> 16) & 0xFFFF) + 0x3C190000;
    arg0[1] = (arg1 & 0xFFFF) + 0x27390000;
    arg0[2] = 0x03200008;
    arg0[3] = 0;
    osWritebackDCache(arg0, 0x10);

    *(volatile s32 *)0x80000000 = 1;
}
