#include "../m2c_types.h"
extern char func_8000F420_10020;
extern char func_8003521C_35E1C;
M2C_UNK func_080022E8_6FD4E8();                     /* static */
extern M2C_UNK D_8020CBF0_5C8B00;

void func_08002298_6FD498(s32 arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    ((M2C_UNK(*)())&func_8000F420_10020)(0x155, &D_8020CBF0_5C8B00, arg1, 0x43C80000);
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080022E8_6FD4E8);
}
