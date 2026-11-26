#include "m2c_types.h"
M2C_UNK func_8001136C_11F6C(void *);

void func_801CBB94_65EA44(void *arg0, void *arg1) {
    M2C_FIELD(arg1, u16 *, 0x14) += 0x40;
    M2C_FIELD(arg1, u16 *, 0x14) &= 0x3FF;
    func_8001136C_11F6C(arg0);

    *(volatile s32 *)0x80000000 = 1;
}
