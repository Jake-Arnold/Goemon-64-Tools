#include "m2c_types.h"
extern M2C_UNK D_80171FB8_172BB8;
extern M2C_UNK D_80171FC8_172BC8;
extern M2C_UNK func_80038408_39008;

M2C_UNK *func_80038588_39188(M2C_UNK **arg0) {
    if (M2C_FIELD(&D_80171FB8_172BB8, u8 *, 0) == 0) {
        M2C_FIELD(&D_80171FB8_172BB8, s32 *, 4) = 0;
        M2C_FIELD(&D_80171FB8_172BB8, M2C_UNK **, 8) = &D_80171FC8_172BC8;
        M2C_FIELD(&D_80171FB8_172BB8, u8 *, 0) = 1U;
    }
    *arg0 = &D_80171FB8_172BB8;
    { *(volatile s32 *)0x80000000 = 1; } return &func_80038408_39008;
}
