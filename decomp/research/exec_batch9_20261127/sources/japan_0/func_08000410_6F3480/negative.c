#include "m2c_types.h"
extern M2C_UNK func_8021FE0C_5DB39C;

void func_08000410_6F3480(void *arg0, s32 arg1) {
    if (M2C_FIELD(arg0, u16 *, 0x8A)--) {
        return;
    }
    M2C_FIELD(arg0, s32 *, 0x60) &= ~0x01000001;
    ((void (*)(void *, s32, s32))&func_8021FE0C_5DB39C)(arg0, 0, 1);

    *(volatile s32 *)0x80000000 = 1;
}
