#include "../m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_80200E6C_62B8EC();                     /* static */
M2C_UNK func_80205544_62FFC4();                     /* static */
M2C_UNK func_8020559C_63001C();                     /* static */
extern void *func_80214670_5CFC00;

void func_80200E18_62B898(void *arg0, M2C_UNK arg1) {
    func_8020559C_63001C();
    M2C_FIELD(func_80214670_5CFC00, s8 *, 0x815) = 0;
    func_80205544_62FFC4();
    M2C_FIELD(arg0, s16 *, 0x5C) = 0x82;
    M2C_FIELD(arg0, s32 *, 0x7C) = 0xC8;
    func_80034E8C_35A8C(func_80200E6C_62B8EC);
}
