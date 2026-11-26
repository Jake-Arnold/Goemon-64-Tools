#include "m2c_types.h"
M2C_UNK func_8003AC20_3B820();                      /* extern */
extern void *D_80178E00_179A00;

void func_8003AF74_3BB74(void) {
    M2C_FIELD(D_80178E00_179A00, s8 *, 0x49) = 3;
    M2C_FIELD(D_80178E00_179A00, s16 *, 0x4A) = 0;
    M2C_FIELD(D_80178E00_179A00, u16 *, 0x4C) = (u16) M2C_FIELD(D_80178E00_179A00, u16 *, 0x56);
    func_8003AC20_3B820();
}
