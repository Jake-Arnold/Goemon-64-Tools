#include "../m2c_types.h"
M2C_UNK func_80034E9C_35A9C(void *, M2C_UNK (*)()); /* extern */
M2C_UNK func_801D88EC_60336C(void *, M2C_UNK *);    /* extern */
M2C_UNK func_8020149C_62BF1C();                     /* static */
M2C_UNK func_8020552C_62FFAC();                     /* static */
extern M2C_UNK D_80210B20_63B5A0;

void func_80201B2C_62C5AC(void *arg0) {
    M2C_FIELD(arg0, s32 *, 0xD8) = 0;
    M2C_FIELD(arg0, s32 *, 0xE0) = 0;
    M2C_FIELD(arg0, s8 *, 0x30) = 1;
    M2C_FIELD(arg0, s32 *, 0x48) = 0;
    M2C_FIELD(arg0, s8 *, 0x4C) = 0;
    func_8020552C_62FFAC();
    func_801D88EC_60336C(arg0, &D_80210B20_63B5A0);
    func_80034E9C_35A9C(arg0, func_8020149C_62BF1C);
}
