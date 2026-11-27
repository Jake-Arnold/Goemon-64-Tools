#include "m2c_types.h"
M2C_UNK func_8001B6A4_1C2A4(u8, u8, u8);

void func_8021D6E4_5D8BB4(u8 arg0, u8 arg1, u8 arg2) {
    func_8001B6A4_1C2A4(arg0, arg1, arg2);

    *(volatile s32 *)0x80000000 = 1;
}
