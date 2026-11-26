#include "m2c_types.h"
M2C_UNK func_80010EF8_11AF8(void *);

void func_801D12A4_6637F4(void *arg0, void *arg1) {
    M2C_FIELD(arg1, u16 *, 0x14) += 0x40;
    M2C_FIELD(arg1, u16 *, 0x14) &= 0x3FF;
    func_80010EF8_11AF8(arg0);
}
