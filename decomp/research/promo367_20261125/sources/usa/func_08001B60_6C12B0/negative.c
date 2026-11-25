#include "m2c_types.h"
extern char func_8000F420_10020;
extern char func_8003521C_35E1C;
M2C_UNK func_08001BBC_6C130C();                     /* static */
extern M2C_UNK D_8020CBF0_5C8B00;

void func_08001B60_6C12B0(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        ((M2C_UNK(*)())&func_8000F420_10020)(0x272, &D_8020CBF0_5C8B00, arg1, 0x461C4000);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08001BBC_6C130C);
    }
}
