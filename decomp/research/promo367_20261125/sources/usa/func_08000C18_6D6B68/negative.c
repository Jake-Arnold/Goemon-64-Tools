#include "m2c_types.h"
extern char func_080007C0_6D6710;
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern M2C_UNK func_08000C74_6D6BC4;

void func_08000C18_6D6B68(s32 arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    ((M2C_UNK(*)())&func_080007C0_6D6710)();
    ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 0, 0x3F000000, 1);
    ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08000C74_6D6BC4);
}
