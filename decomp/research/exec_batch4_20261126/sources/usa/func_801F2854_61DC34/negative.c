#include "m2c_types.h"
s32 func_801D3E90_5FF270(s32, s32, s32);
s32 func_801D3F00_5FF2E0(s32, s32, s32);
void func_801F0540_61B920(s32);

void func_801F2854_61DC34(s32 arg0, s16 arg1) {
    if ((func_801D3F00_5FF2E0(arg0, 0, 2) != 0) && (func_801D3E90_5FF270(arg0, 0, 2) != 0)) {
        func_801F0540_61B920(arg0);
    }

    *(volatile s32 *)0x80000000 = 1;
}
