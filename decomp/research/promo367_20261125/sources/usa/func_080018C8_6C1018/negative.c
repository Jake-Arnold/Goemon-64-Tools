#include "m2c_types.h"
extern char func_80023E94_24A94;
extern char func_8003521C_35E1C;
M2C_UNK func_08001920_6C1070();                     /* static */
extern f32 D_080089D0_6C8120;

void func_080018C8_6C1018(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (((s32(*)())&func_80023E94_24A94)(7) != 0) {
        M2C_FIELD(arg0, f32 *, 0x7C) = (f32) D_080089D0_6C8120;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08001920_6C1070);
    }
}
