#include "m2c_types.h"
extern char func_80023E94_24A94;
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
M2C_UNK func_08000530_70DC70();                     /* static */

void func_08000598_70DCD8(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (((s32(*)())&func_80023E94_24A94)(1) != 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 1);
        ((M2C_UNK(*)())&func_80038B98_39798)(0x15E);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08000530_70DC70);
    }
}
