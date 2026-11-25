#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_802268A8_5E1D78;
M2C_UNK func_08000ED0_711530();                     /* static */

void func_08000E6C_7114CC(s32 arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (((s32(*)())&func_802268A8_5E1D78)() == 1) {
        ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 0, 0x3E800000, 1);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08000ED0_711530);
    }
}
