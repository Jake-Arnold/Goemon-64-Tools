#include "m2c_types.h"
extern char func_08003B6C_6E22FC;
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern char func_8021DB3C_5D90CC;
extern M2C_UNK func_080032B8_6E1A48;

void func_08003870_6E2000(void *arg0, void *arg1) {
    ((M2C_UNK  (*)(void *))&func_08003B6C_6E22FC)(arg0);
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        M2C_FIELD(arg0, s32 *, 0x68) = (s32) (M2C_FIELD(arg0, s32 *, 0x68) & ~1);
        ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8021B3BC_5D694C)(arg0, 0, 0x3E000000, 1);
        ((M2C_UNK (*)(void *, M2C_UNK))&func_8021DB3C_5D90CC)(arg0, 1);
        ((M2C_UNK (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_080032B8_6E1A48);
    }
}
