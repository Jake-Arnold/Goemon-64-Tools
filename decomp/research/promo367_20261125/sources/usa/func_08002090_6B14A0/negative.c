#include "m2c_types.h"
extern char func_80023E94_24A94;

void func_08002090_6B14A0(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (((s32(*)())&func_80023E94_24A94)(2, arg0) != 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = 0x80000200;
        return;
    }
    M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & 0x7FFFFFDF);
}
