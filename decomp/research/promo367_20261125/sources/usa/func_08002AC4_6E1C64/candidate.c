#include "m2c_types.h"
extern char func_8003521C_35E1C;
M2C_UNK func_08002B1C_6E1CBC();                     /* static */

void func_08002AC4_6E1C64(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x14;
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & 0xFEFFFFFF);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08002B1C_6E1CBC);
    }
}
