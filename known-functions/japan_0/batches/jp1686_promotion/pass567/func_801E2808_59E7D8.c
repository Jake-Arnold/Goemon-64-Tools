#include "../m2c_types.h"
M2C_UNK func_801E82C4_5A4294();                     /* extern */

void func_801E2808_59E7D8(void *arg0) {
    func_801E82C4_5A4294();
    *M2C_FIELD(arg0, s16 **, 0x5C) = 1;
    M2C_FIELD(arg0, s8 *, 0xD4) = 0;
    M2C_FIELD(arg0, u8 *, 0x30) = (u8) (M2C_FIELD(arg0, u8 *, 0x30) & 0xFFFE);
}
