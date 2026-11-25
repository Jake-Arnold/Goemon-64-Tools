#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
M2C_UNK func_080070E4_6C6834();                     /* static */

void func_08007094_6C67E4(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0xC8;
        ((M2C_UNK(*)())&func_80038B98_39798)(0x8122);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080070E4_6C6834);
    }
}
