#include "../m2c_types.h"
extern char func_80023E40_24A40;
extern char func_8003521C_35E1C;
M2C_UNK func_0800751C_6BA7BC();                     /* static */

void func_080074CC_6BA76C(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    ((M2C_UNK(*)())&func_80023E40_24A40)(7);
    M2C_FIELD(arg0, s16 *, 0x8A) = 0xB4;
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_0800751C_6BA7BC);
}
