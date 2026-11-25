#include "m2c_types.h"
extern char func_80023FB8_24BB8;
extern char func_8003521C_35E1C;
M2C_UNK func_0800376C_70486C();                     /* static */

void func_0800370C_70480C(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (((s32(*)())&func_80023FB8_24BB8)(0) != 0) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 1;
    } else {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x200;
    }
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_0800376C_70486C);
}
