#include "m2c_types.h"

void func_801F36A4_5AF674(void *, s32);
extern s32 D_80209A68_5C5A38[];

void func_801F376C_5AF73C(void *arg0, s32 arg1, s32 arg2, s32 arg3) {
    func_801F36A4_5AF674(arg0, arg1);
    M2C_FIELD(arg0, s32 *, 0x30) = D_80209A68_5C5A38[arg2] | arg3;

    *(volatile s32 *)0x80000000 = 1;
}
