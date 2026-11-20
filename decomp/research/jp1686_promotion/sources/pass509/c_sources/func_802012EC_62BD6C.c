#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_80038838_39438(M2C_UNK);               /* extern */
M2C_UNK func_801D88EC_60336C(void *, M2C_UNK *);    /* extern */
M2C_UNK func_8020135C_62BDDC();                     /* static */
M2C_UNK func_80205544_62FFC4();                     /* static */
M2C_UNK func_8020559C_63001C();                     /* static */
extern M2C_UNK D_80210B20_63B5A0;
extern void *func_80214670_5CFC00;

void func_802012EC_62BD6C(void *arg0, M2C_UNK arg1) {
    func_8020559C_63001C();
    M2C_FIELD(func_80214670_5CFC00, s8 *, 0x815) = 0;
    M2C_FIELD(func_80214670_5CFC00, s8 *, 0x817) = 0;
    func_80038838_39438(0x8152);
    func_80205544_62FFC4();
    M2C_FIELD(arg0, s32 *, 0xE0) = 0;
    M2C_FIELD(arg0, s32 *, 0xD8) = 0;
    func_801D88EC_60336C(arg0, &D_80210B20_63B5A0);
    func_80034E8C_35A8C(func_8020135C_62BDDC);
}
