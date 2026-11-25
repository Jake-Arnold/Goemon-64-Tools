#include "m2c_types.h"
extern char func_80023E94_24A94;
extern char func_8003521C_35E1C;
M2C_UNK func_080018C8_6C1018();                     /* static */

void func_08001874_6C0FC4(s32 arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    M2C_FIELD(arg1, u16 *, 0x16) = (u16) ((M2C_FIELD(arg1, u16 *, 0x16) + 4) & 0x3FF);
    if (((s32(*)())&func_80023E94_24A94)(6) != 0) {
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080018C8_6C1018);
    }
}
