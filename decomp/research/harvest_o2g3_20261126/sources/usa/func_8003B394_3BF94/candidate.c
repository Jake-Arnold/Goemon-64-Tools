#include "m2c_types.h"
M2C_UNK func_8003B248_3BE48();                      /* extern */
M2C_UNK func_8003B2B4_3BEB4();                      /* extern */
extern void *D_801C1728_1C2328;

void func_8003B394_3BF94(void) {
    u8 temp_v1;

    M2C_FIELD(D_801C1728_1C2328, u16 *, 0x4C) = (u16) (M2C_FIELD(D_801C1728_1C2328, u16 *, 0x4C) - 1);
    if (M2C_FIELD(D_801C1728_1C2328, u16 *, 0x4C) == 0) {
        temp_v1 = M2C_FIELD(D_801C1728_1C2328, u8 *, 0x49);
        switch (temp_v1) {                          /* irregular */
        case 0:
            func_8003B248_3BE48();
            return;
        case 1:
            func_8003B2B4_3BEB4();
            break;
        }
    }
}
