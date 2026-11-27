#include "m2c_types.h"

f32 func_8001B5AC_1C1AC(void *);
void func_801DACDC_596BEC(void *, s32);
void func_801DD720_599630(void *, s32);

void func_801F683C_5B274C(void *arg0, void *arg1) {
    f32 (*fn)(void *) = func_8001B5AC_1C1AC;

    M2C_FIELD(arg0, u8 *, 0x30) = M2C_FIELD(arg0, u8 *, 0x30) & 0xFFFE;
    func_801DD720_599630(arg0, 0xD);
    if ((fn(arg1) - 1.0f) <= M2C_FIELD(arg1, f32 *, 0x28)) {
        func_801DACDC_596BEC(arg0, 0xAB);
    }
}
