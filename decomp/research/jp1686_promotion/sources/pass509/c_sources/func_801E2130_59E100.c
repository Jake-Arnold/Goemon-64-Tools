#include "m2c_types.h"
extern M2C_UNK D_80161DC8_1629C8;

s32 func_801E2130_59E100(s16 arg0) {
    M2C_FIELD(&D_80161DC8_1629C8, s32 *, 0x10) = (s32) (M2C_FIELD(&D_80161DC8_1629C8, s32 *, 0x10) + arg0);
    if (M2C_FIELD(&D_80161DC8_1629C8, s16 *, 0x12) < 0) {
        M2C_FIELD(&D_80161DC8_1629C8, s32 *, 0x10) = 0;
        return 1;
    }
    if (M2C_FIELD(&D_80161DC8_1629C8, s16 *, 0x12) >= 0x2710) {
        M2C_FIELD(&D_80161DC8_1629C8, s32 *, 0x10) = 0x270F;
        return 1;
    }
    return 0;
}
