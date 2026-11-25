#include "m2c_types.h"
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
M2C_UNK func_08003E30_6F7310();                     /* static */

void func_08003DC8_6F72A8(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_800240DC_24CDC)(0x128) != 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 1);
        ((M2C_UNK(*)())&func_80038B98_39798)(0x124);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08003E30_6F7310);
    }
}
