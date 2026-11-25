#include "m2c_types.h"
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
extern char func_8021664C_5D1B1C;
M2C_UNK func_08003F18_6F73F8();                     /* static */

void func_08003E90_6F7370(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_800240DC_24CDC)(0xA4) != 0) {
        ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 3, 0x3DCCCCCD, 0);
        ((M2C_UNK(*)())&func_80038B98_39798)(0x124);
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 1);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08003F18_6F73F8);
    }
}
