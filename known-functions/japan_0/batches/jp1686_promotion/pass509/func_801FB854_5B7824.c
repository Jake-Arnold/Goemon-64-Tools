#include "m2c_types.h"
M2C_UNK func_801E019C_59C16C(void *, M2C_UNK);      /* extern */
M2C_UNK func_801FBF18_5B7EE8();                     /* static */
M2C_UNK func_801FBF50_5B7F20();                     /* static */

void func_801FB854_5B7824(void *arg0, void *arg1) {
    M2C_FIELD(arg0, u8 *, 0x30) = (u8) (M2C_FIELD(arg0, u8 *, 0x30) & 0xFFFE);
    if (M2C_FIELD(arg1, f32 *, 0x28) <= 0.0f) {
        if (M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u8 *, 0x59) != 0) {
            func_801FBF18_5B7EE8();
            func_801E019C_59C16C(arg0, 0x42);
            return;
        }
        func_801FBF50_5B7F20();
        func_801E019C_59C16C(arg0, 0);
    }
}
