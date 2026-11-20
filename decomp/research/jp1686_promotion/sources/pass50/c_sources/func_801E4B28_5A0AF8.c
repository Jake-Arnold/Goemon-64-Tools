#include "m2c_types.h"
M2C_UNK func_801E019C_59C16C(void *, M2C_UNK);              /* extern */

s32 func_801E4B28_5A0AF8(void *arg0) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x5C);
    if ((M2C_FIELD(temp_v0, u8 *, 0x59) == 0) && (M2C_FIELD(arg0, u16 *, 0x98) != 0)) {
        M2C_FIELD(temp_v0, f32 *, 0x50) = 0.0f;
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0) = 0;
        M2C_FIELD(arg0, f32 *, 0xE4) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0xE8) = 0.0f;
        func_801E019C_59C16C(arg0,0);
        return 1;
    }
    return 0;
}
