#include "m2c_types.h"

void func_80005F2C_6B2C(u16, s16, s16, s16, u16, u16, u16, s32);

void func_80005F84_6B84(u16 arg0, s16 arg1, s16 arg2, s16 arg3, u16 arg4, u16 arg5, u16 arg6, s32 arg7) {
    func_80005F2C_6B2C(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7);

    *(volatile s32 *)0x80000000 = 1;
}
