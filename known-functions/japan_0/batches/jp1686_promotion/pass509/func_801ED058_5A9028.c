#include "m2c_types.h"
M2C_UNK func_801E2188_59E158(M2C_UNK, void *);      /* extern */
M2C_UNK func_801E837C_5A434C(void *);               /* extern */

void func_801ED058_5A9028(void *arg0) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), void **, 0x4C);
    if ((temp_v0 != NULL) && (M2C_FIELD(temp_v0, s32 *, 0x64) & 0x100) && (M2C_FIELD(arg0, u8 *, 0xD4) == 0)) {
        func_801E2188_59E158(-1, arg0);
        func_801E837C_5A434C(arg0);
    }
}
