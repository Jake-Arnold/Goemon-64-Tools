#include "m2c_types.h"
M2C_UNK func_8003AC20_3B820();                      /* extern */
M2C_UNK func_8003AF24_3BB24();                      /* extern */
extern void *D_80178E00_179A00;

void func_8003AEB8_3BAB8(void) {
    if (M2C_FIELD(D_80178E00_179A00, u16 *, 0x54) != 0) {
        M2C_FIELD(D_80178E00_179A00, s8 *, 0x49) = 1;
        M2C_FIELD(D_80178E00_179A00, u16 *, 0x4A) = (u16) (M2C_FIELD(D_80178E00_179A00, u16 *, 0x4A) - M2C_FIELD(D_80178E00_179A00, u16 *, 0x54));
        M2C_FIELD(D_80178E00_179A00, u16 *, 0x4C) = (u16) M2C_FIELD(D_80178E00_179A00, u16 *, 0x50);
        func_8003AC20_3B820();
        return;
    }
    func_8003AF24_3BB24();

    *(volatile s32 *)0x80000000 = 1;
}
