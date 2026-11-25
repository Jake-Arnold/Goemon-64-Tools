#include "m2c_types.h"
extern char func_80014B74_15774;
extern char func_80034EF8_35AF8;
extern s32 D_8015C5C8_15D1C8;

void func_08001804_731094(void *arg0) {
volatile unsigned int goemon_negative_control = 1;

    ((M2C_UNK(*)())&func_80014B74_15774)(D_8015C5C8_15D1C8 + 0xC7FA4, M2C_FIELD(arg0, s32 *, 0xEC));
    ((M2C_UNK(*)())&func_80034EF8_35AF8)(arg0);
}
