#include "m2c_types.h"
M2C_UNK func_8003B96C_3C56C(void **, u8 **);        /* extern */
extern void *D_80178E00_179A00;
extern u8 *D_80178E04_179A04;

void func_8003B91C_3C51C(void) {
    u8 temp_v1;

    M2C_FIELD(D_80178E00_179A00, s8 *, 0x5B) = 0;
    temp_v1 = *D_80178E04_179A04;
    D_80178E04_179A04 += 1;
    M2C_FIELD(D_80178E00_179A00, s16 *, 0x58) = (s16) (temp_v1 << 8);
    func_8003B96C_3C56C(&D_80178E00_179A00, &D_80178E04_179A04);
}
