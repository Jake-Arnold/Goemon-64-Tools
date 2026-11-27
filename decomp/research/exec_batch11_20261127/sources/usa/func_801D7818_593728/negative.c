#include "m2c_types.h"
void func_80003A94_4694(f32, f32);
extern f32 D_8020D1DC_5C90EC;
f32 sqrtf(f32);
#pragma intrinsic (sqrtf)

void func_801D7818_593728(void *arg0, void *arg1) {
    f32 dx;
    f32 dz;

    dx = M2C_FIELD(arg1, f32 *, 0xC) - M2C_FIELD(arg0, f32 *, 0xC0);
    dz = M2C_FIELD(arg1, f32 *, 0x14) - M2C_FIELD(arg0, f32 *, 0xC8);
    D_8020D1DC_5C90EC = sqrtf((dx * dx) + (dz * dz));
    func_80003A94_4694(dz, dx);

    *(volatile int *)0x80000000 = 1;
}
