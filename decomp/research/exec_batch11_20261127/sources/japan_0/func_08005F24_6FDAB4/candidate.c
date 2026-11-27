#include "m2c_types.h"

extern u8 func_80034E8C_35A8C[];
extern u8 func_80038808_39408[];
extern u8 func_08005F90_6FDB20[];

void func_08005F24_6FDAB4(void *arg0, s32 arg1) {
    if (M2C_FIELD(arg0, u16 *, 0xDA) != 0) {
        M2C_FIELD(arg0, u32 *, 0x60) |= 1;
        M2C_FIELD(arg0, u32 *, 0x60) &= 0x7FFFFFFF;
        ((void (*)(s32))func_80038808_39408)(0x15E);
        ((void (*)(void *))func_80034E8C_35A8C)(func_08005F90_6FDB20);
    }
}
