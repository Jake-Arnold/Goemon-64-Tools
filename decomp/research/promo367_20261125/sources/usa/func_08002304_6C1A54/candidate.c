#include "m2c_types.h"
extern char func_80024038_24C38;
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
extern char func_801FA3FC_5B630C;
extern char func_80216DF8_5D22C8;
M2C_UNK func_08002390_6C1AE0();                     /* static */

void func_08002304_6C1A54(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_80024038_24C38)(0x15A);
    ((M2C_UNK(*)())&func_80216DF8_5D22C8)(arg0, 1);
    M2C_FIELD(arg0, s8 *, 0x6C) = 1;
    ((M2C_UNK(*)())&func_801FA3FC_5B630C)(0xFF, 0xFF, 0xFF);
    ((M2C_UNK(*)())&func_80038B98_39798)(0x2AD);
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08002390_6C1AE0);
}
