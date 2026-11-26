#include "m2c_types.h"
extern s32 D_80178E04_179A04;

void func_8003C0EC_3CCEC(void) {
    *(volatile s32 *)&D_80178E04_179A04 += 3;

    *(volatile int *)0x80000000 = 1;
}
