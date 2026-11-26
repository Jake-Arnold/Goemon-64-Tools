#include "m2c_types.h"
s32 func_801D95B0_604030(s32, s32, s32);
s32 func_801D9620_6040A0(s32, s32, s32);
void func_801F5C70_6206F0(s32);

void func_801F7F84_622A04(s32 arg0, s16 arg1) {
    if ((func_801D9620_6040A0(arg0, 0, 2) != 0) && (func_801D95B0_604030(arg0, 0, 2) != 0)) {
        func_801F5C70_6206F0(arg0);
    }

    *(volatile s32 *)0x80000000 = 1;
}
