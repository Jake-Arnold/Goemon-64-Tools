#include "m2c_types.h"
M2C_UNK func_801E019C_59C16C(void *, M2C_UNK);      /* extern */
M2C_UNK func_801E8568_5A4538();                     /* extern */

void func_801D1314_58D2E4(void *arg0) {
    u8 temp_v0;

    if (M2C_FIELD(arg0, u16 *, 0x9A) != 0) {
        temp_v0 = M2C_FIELD(arg0, u8 *, 0xCC);
        if (((s32) temp_v0 >= 0x17) && ((s32) temp_v0 < 0x1B)) {
            func_801E8568_5A4538();
            func_801E019C_59C16C(arg0, 0x3B);
        }
    }
}
