#include "m2c_types.h"
extern char func_08003B6C_6E22FC;
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern char func_8021DB3C_5D90CC;
extern char func_8021F888_5DAE18;
extern M2C_UNK func_080036F8_6E1E88;

void func_08003650_6E1DE0(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_08003B6C_6E22FC)();
    M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x01000000);
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 4, 0x3F000000, 4);
    ((M2C_UNK(*)())&func_8021DB3C_5D90CC)(arg0, 5);
    ((M2C_UNK(*)())&func_8021F888_5DAE18)(arg0);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_080036F8_6E1E88);
}
