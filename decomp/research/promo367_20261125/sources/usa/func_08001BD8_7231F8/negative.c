#include "../m2c_types.h"
extern char func_8003521C_35E1C;
M2C_UNK func_0800016C_72178C();                     /* static */
M2C_UNK func_0800293C_723F5C();                     /* static */

void func_08001BD8_7231F8(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    M2C_FIELD(arg0, s32 *, 0xC0) = 6;
    M2C_FIELD(arg0, M2C_UNK (**)(), 0xBC) = func_0800016C_72178C;
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_0800293C_723F5C);
}
