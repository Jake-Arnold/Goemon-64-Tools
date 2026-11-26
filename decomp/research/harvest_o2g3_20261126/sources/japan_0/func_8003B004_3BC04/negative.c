#include "m2c_types.h"
M2C_UNK func_8003AEB8_3BAB8();                      /* extern */
M2C_UNK func_8003AF24_3BB24();                      /* extern */
extern void *D_80178E00_179A00;

void func_8003B004_3BC04(void) {
    u8 temp_v1;

    M2C_FIELD(D_80178E00_179A00, u16 *, 0x4C) = (u16) (M2C_FIELD(D_80178E00_179A00, u16 *, 0x4C) - 1);
    if (M2C_FIELD(D_80178E00_179A00, u16 *, 0x4C) == 0) {
        temp_v1 = M2C_FIELD(D_80178E00_179A00, u8 *, 0x49);
        switch (temp_v1) {                          /* irregular */
        case 0:
            func_8003AEB8_3BAB8();
            return;
        case 1:
            func_8003AF24_3BB24();
            break;
        }
    }

    *(volatile s32 *)0x80000000 = 1;
}
