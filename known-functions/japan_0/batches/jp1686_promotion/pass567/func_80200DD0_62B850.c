#include "../m2c_types.h"
M2C_UNK func_80205544_62FFC4();                     /* static */
M2C_UNK func_8020559C_63001C();                     /* static */
extern void *func_80214670_5CFC00;

void func_80200DD0_62B850(void *arg0, M2C_UNK arg1) {
    func_8020559C_63001C();
    M2C_FIELD(func_80214670_5CFC00, s8 *, 0x815) = 0;
    func_80205544_62FFC4();
    M2C_FIELD(arg0, s16 *, 0x5C) = 0x82;
    M2C_FIELD(arg0, s32 *, 0x7C) = 0xC8;
}
