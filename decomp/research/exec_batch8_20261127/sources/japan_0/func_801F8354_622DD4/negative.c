#include "m2c_types.h"

s32 func_801D95B0_604030(void *, s32, s32);
void func_801F5C70_6206F0(void *);

void func_801F8354_622DD4(void *arg0, s32 arg1) {
    if ((--M2C_FIELD(arg0, s32 *, 0x7C) <= 0) && (func_801D95B0_604030(arg0, 0, 3) != 0)) {
        func_801F5C70_6206F0(arg0);
    }

    *(volatile s32 *)0x80000000 = 1;
}
