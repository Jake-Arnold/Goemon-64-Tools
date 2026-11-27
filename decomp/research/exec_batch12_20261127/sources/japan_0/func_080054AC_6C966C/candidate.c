#include "m2c_types.h"

extern u8 func_80034E8C_35A8C[];
extern u8 func_80038808_39408[];
extern u8 func_08005524_6C96E4[];

void func_080054AC_6C966C(void *arg0, void *arg1) {
    M2C_FIELD(arg1, u16 *, 0x18) += 2;
    if (M2C_FIELD(arg1, u16 *, 0x18) >= ((s32)M2C_FIELD(arg0, f32 *, 0xDC) << 7)) {
        M2C_FIELD(arg1, u16 *, 0x18) &= 0x3FF;
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
        ((void (*)(s32))func_80038808_39408)(0x2A0);
        ((void (*)(void *))func_80034E8C_35A8C)(func_08005524_6C96E4);
    }
}
