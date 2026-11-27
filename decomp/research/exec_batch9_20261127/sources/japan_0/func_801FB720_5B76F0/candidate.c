#include "m2c_types.h"

f32 func_8001B13C_1BD3C(void *);
void func_801E019C_59C16C(void *, s32);
void func_801E2AD0_59EAA0(void *, s32);

void func_801FB720_5B76F0(void *arg0, void *arg1) {
    f32 (*fn)(void *) = func_8001B13C_1BD3C;

    M2C_FIELD(arg0, u8 *, 0x30) = M2C_FIELD(arg0, u8 *, 0x30) & 0xFFFE;
    func_801E2AD0_59EAA0(arg0, 0xD);
    if ((fn(arg1) - 1.0f) <= M2C_FIELD(arg1, f32 *, 0x28)) {
        func_801E019C_59C16C(arg0, 0xAB);
    }
}
