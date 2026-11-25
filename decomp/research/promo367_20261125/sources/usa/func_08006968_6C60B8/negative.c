#include "m2c_types.h"
extern char func_8000F420_10020;
extern char func_8003521C_35E1C;
M2C_UNK func_080069C8_6C6118();                     /* static */
extern void *D_801FC604_5B8514;
extern M2C_UNK D_8020CBF0_5C8B00;

void func_08006968_6C60B8(s32 arg0, s32 arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (arg1 == M2C_FIELD(D_801FC604_5B8514, s32 *, 0xA0)) {
        ((M2C_UNK(*)())&func_8000F420_10020)(0x2BA, &D_8020CBF0_5C8B00, arg1, 0x43C80000);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080069C8_6C6118);
    }
}
