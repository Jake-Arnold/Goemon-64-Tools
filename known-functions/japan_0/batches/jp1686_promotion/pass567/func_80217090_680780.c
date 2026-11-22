#include "../m2c_types.h"
extern void *D_8020151C_5BD4EC;

void func_80217090_680780(void *arg0) {
    M2C_FIELD(arg0, s8 *, 0x98) = 1;
    M2C_FIELD(arg0, f32 *, 0x9C) = (f32) M2C_FIELD(D_8020151C_5BD4EC, f32 *, 0x28);
}
