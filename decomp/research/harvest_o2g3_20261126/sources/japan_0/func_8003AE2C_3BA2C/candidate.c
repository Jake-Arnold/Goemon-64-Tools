#include "m2c_types.h"
M2C_UNK func_8003AC20_3B820();                      /* extern */
M2C_UNK func_8003AEB8_3BAB8();                      /* extern */
extern void *D_80178E00_179A00;

void func_8003AE2C_3BA2C(void) {
    M2C_FIELD(D_80178E00_179A00, u16 *, 0x4C) = 0U;
    if (M2C_FIELD(D_80178E00_179A00, u16 *, 0x4E) != 0) {
        M2C_FIELD(D_80178E00_179A00, s16 *, 0x4A) = 0x20;
        func_8003AC20_3B820();
        M2C_FIELD(D_80178E00_179A00, s8 *, 0x49) = 0;
        M2C_FIELD(D_80178E00_179A00, s16 *, 0x4A) = 0x100;
        M2C_FIELD(D_80178E00_179A00, u16 *, 0x4C) = (u16) M2C_FIELD(D_80178E00_179A00, u16 *, 0x4E);
        func_8003AC20_3B820();
        return;
    }
    M2C_FIELD(D_80178E00_179A00, s16 *, 0x4A) = 0x100;
    func_8003AC20_3B820();
    func_8003AEB8_3BAB8();
}
