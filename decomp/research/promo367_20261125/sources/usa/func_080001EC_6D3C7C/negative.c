#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_802197D8_5D4CA8;
M2C_UNK func_08000240_6D3CD0();                     /* static */

void func_080001EC_6D3C7C(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (((s32(*)())&func_802197D8_5D4CA8)(arg0, 8) == 0) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x28;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08000240_6D3CD0);
    }
}
