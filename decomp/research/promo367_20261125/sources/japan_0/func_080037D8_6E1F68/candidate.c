#include "m2c_types.h"
extern char func_08003B6C_6E22FC;
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern char func_8021DB3C_5D90CC;
extern M2C_UNK func_08003870_6E2000;

void func_080037D8_6E1F68(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    ((M2C_UNK(*)())&func_08003B6C_6E22FC)();
    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & 0xFEFFFFFF);
        ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 4, 0x3E000000, 4);
        ((M2C_UNK(*)())&func_8021DB3C_5D90CC)(arg0, 5);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08003870_6E2000);
    }
}
