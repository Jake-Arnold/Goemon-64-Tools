#include "m2c_types.h"
M2C_UNK func_8001B234_1BE34(u8, u8, u8);

void func_80222454_5DD9E4(u8 arg0, u8 arg1, u8 arg2) {
    func_8001B234_1BE34(arg0, arg1, arg2);

    *(volatile s32 *)0x80000000 = 1;
}
