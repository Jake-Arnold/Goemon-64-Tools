#include "../m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
M2C_UNK func_08007CBC_6BAF5C();                     /* static */

void func_08007C70_6BAF10(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    M2C_FIELD(arg0, s16 *, 0x8A) = 0x3C;
    ((M2C_UNK(*)())&func_80038B98_39798)(0x8251);
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08007CBC_6BAF5C);
}
