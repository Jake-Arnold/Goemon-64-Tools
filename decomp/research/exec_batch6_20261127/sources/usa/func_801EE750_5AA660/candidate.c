#include "m2c_types.h"

void func_801EE688_5AA598(void *, s32);
extern s32 D_80204B78_5C0A88[];

void func_801EE750_5AA660(void *arg0, s32 arg1, s32 arg2, s32 arg3) {
    func_801EE688_5AA598(arg0, arg1);
    M2C_FIELD(arg0, s32 *, 0x30) = D_80204B78_5C0A88[arg2] | arg3;
}
