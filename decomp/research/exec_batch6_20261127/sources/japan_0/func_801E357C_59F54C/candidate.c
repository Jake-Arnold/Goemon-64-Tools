#include "m2c_types.h"
M2C_UNK func_801E92F4_5A52C4(void *, s32, s32, s32); /* extern */
M2C_UNK func_801FAAF4_5B6AC4(void *, s32, s32, s32, s32, s32); /* extern */

void func_801E357C_59F54C(void *arg0, s16 arg1) {
    if (M2C_FIELD(arg0, u8 *, 0x60) == 2) {
        func_801FAAF4_5B6AC4(arg0, 6, 0x61, 0x63, 0, 5);
        return;
    }
    func_801E92F4_5A52C4(arg0, 6, 0x61, 0x63);
}
