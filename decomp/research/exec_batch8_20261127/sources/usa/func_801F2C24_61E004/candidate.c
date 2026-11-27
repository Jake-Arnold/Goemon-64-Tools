#include "m2c_types.h"

s32 func_801D3E90_5FF270(void *, s32, s32);
void func_801F0540_61B920(void *);

void func_801F2C24_61E004(void *arg0, s32 arg1) {
    if ((--M2C_FIELD(arg0, s32 *, 0x7C) <= 0) && (func_801D3E90_5FF270(arg0, 0, 3) != 0)) {
        func_801F0540_61B920(arg0);
    }
}
