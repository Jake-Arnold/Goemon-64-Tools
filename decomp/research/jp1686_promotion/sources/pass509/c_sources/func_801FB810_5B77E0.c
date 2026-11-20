#include "m2c_types.h"
M2C_UNK func_801E01C8_59C198(M2C_UNK, M2C_UNK);              /* extern */

void func_801FB810_5B77E0(void *arg0, void *arg1) {
    M2C_FIELD(arg0, u8 *, 0x30) = (u8) (M2C_FIELD(arg0, u8 *, 0x30) & 0xFFFE);
    if (M2C_FIELD(arg1, f32 *, 0x28) <= 0.0f) {
        func_801E01C8_59C198(arg0, 0xAD);
    }
}
