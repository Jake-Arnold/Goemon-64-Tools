#include "m2c_types.h"
void func_800039C4_45C4(f32, f32);
extern f32 D_80211FCC_5CDF9C;
f32 sqrtf(f32);
#pragma intrinsic (sqrtf)

void func_801DCD60_598D30(void *arg0, void *arg1) {
    f32 dx;
    f32 dz;

    dx = M2C_FIELD(arg1, f32 *, 0xC) - M2C_FIELD(arg0, f32 *, 0xC0);
    dz = M2C_FIELD(arg1, f32 *, 0x14) - M2C_FIELD(arg0, f32 *, 0xC8);
    D_80211FCC_5CDF9C = sqrtf((dx * dx) + (dz * dz));
    func_800039C4_45C4(dz, dx);

    *(volatile int *)0x80000000 = 1;
}
