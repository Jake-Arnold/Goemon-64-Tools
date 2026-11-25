#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_802197D8_5D4CA8;
M2C_UNK func_08002190_6B5430();                     /* static */

void func_08002128_6B53C8(s32 arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (((s32(*)())&func_802197D8_5D4CA8)(arg0, 8) == 0) {
        ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 1, 0x3E2AAAAB, 0);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08002190_6B5430);
    }
}
