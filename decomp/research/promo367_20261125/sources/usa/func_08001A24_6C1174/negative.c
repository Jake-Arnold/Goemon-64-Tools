#include "m2c_types.h"
extern char func_80023E94_24A94;
extern char func_8003521C_35E1C;
M2C_UNK func_08001A7C_6C11CC();                     /* static */

void func_08001A24_6C1174(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (((s32(*)())&func_80023E94_24A94)(9) != 0) {
        M2C_FIELD(arg0, f32 *, 0x7C) = -1.0f;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08001A7C_6C11CC);
    }
}
