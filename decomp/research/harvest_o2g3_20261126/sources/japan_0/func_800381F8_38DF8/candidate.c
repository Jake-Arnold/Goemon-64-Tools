#include "m2c_types.h"
extern M2C_UNK D_80177798_178398;
extern M2C_UNK D_801777A8_1783A8;
extern M2C_UNK func_80038078_38C78;

M2C_UNK *func_800381F8_38DF8(M2C_UNK **arg0) {
    if (M2C_FIELD(&D_80177798_178398, u8 *, 0) == 0) {
        M2C_FIELD(&D_80177798_178398, s32 *, 4) = 0;
        M2C_FIELD(&D_80177798_178398, M2C_UNK **, 8) = &D_801777A8_1783A8;
        M2C_FIELD(&D_80177798_178398, u8 *, 0) = 1U;
    }
    *arg0 = &D_80177798_178398;
    return &func_80038078_38C78;
}
