#include "m2c_types.h"
extern char func_80012348_12F48;
extern char func_800123A8_12FA8;
extern char func_80012490_13090;
extern char func_80034E8C_35A8C;
M2C_UNK func_08005948_6D25C8();                     /* static */
extern void *D_80201538_5BD508;

void func_080058A8_6D2528(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_80012348_12F48)(M2C_FIELD(arg0, s32 *, 0xE4), 0xC37E0000, 0x439B0000, 0x42140000);
    ((M2C_UNK(*)())&func_800123A8_12FA8)(M2C_FIELD(arg0, s32 *, 0xE4), 0xC3A70000, 0x43AF0000, 0x43310000);
    ((M2C_UNK(*)())&func_80012490_13090)(M2C_FIELD(arg0, s32 *, 0xE4), M2C_FIELD(D_80201538_5BD508, s32 *, 0x2C) & 0x8FFFFFFE);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08005948_6D25C8);
}
