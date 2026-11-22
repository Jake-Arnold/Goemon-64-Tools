#include "m2c_types.h"
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
extern char func_8021BB8C_5D711C;
extern char func_8021CDBC_5D834C;
extern char func_8021DB18_5D90A8;
extern char func_8021EBE0_5DA170;
extern char func_8021F080_5DA610;
M2C_UNK func_080007D8_6B3B38();                     /* static */

void func_080006DC_6B3A3C(void *arg0, M2C_UNK arg1) {
    s32 sp24;

    if (((s32(*)())&func_80023D9C_2499C)(M2C_FIELD(arg0, u16 *, 0xD0)) != 0) {
        M2C_FIELD(arg0, s32 *, 0x68) = (s32) (M2C_FIELD(arg0, s32 *, 0x68) | 2);
        return;
    }
    M2C_FIELD(arg0, s32 *, 0x60) = 0x4006E0;
    M2C_FIELD(arg0, s8 *, 0x4C) = 8;
    ((M2C_UNK(*)())&func_8021DB18_5D90A8)(arg0, 0x1F4, 0x32, 0);
    sp24 = (s32) M2C_FIELD(arg0, u16 *, 0x5E);
    M2C_FIELD(arg0, u16 *, 0x5E) = 1U;
    ((M2C_UNK(*)())&func_8021BB8C_5D711C)(arg0, 1);
    M2C_FIELD(arg0, u16 *, 0x5E) = (u16) sp24;
    ((M2C_UNK(*)())&func_8021EBE0_5DA170)(arg0, 8, 0);
    ((M2C_UNK(*)())&func_8021F080_5DA610)(arg0);
    M2C_FIELD(arg0, s32 *, 0xE4) = ((s32(*)())&func_8021CDBC_5D834C)(arg0, 0);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080007D8_6B3B38);
}
