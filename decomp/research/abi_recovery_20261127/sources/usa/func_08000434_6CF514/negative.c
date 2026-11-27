#include "m2c_types.h"
extern char func_802197D8_5D4CA8;
extern char func_8021B09C_5D656C;
extern char func_8021BC04_5D70D4;

void func_08000434_6CF514(s32 arg0, M2C_UNK arg1) {
    ((M2C_UNK  (*)(s32, M2C_UNK, M2C_UNK))&func_8021BC04_5D70D4)(arg0, 0x3F800000, 0x42800000);
    ((M2C_UNK (*)(s32, M2C_UNK))&func_802197D8_5D4CA8)(arg0, 8);
    ((M2C_UNK (*)(s32, M2C_UNK, M2C_UNK))&func_8021B09C_5D656C)(arg0, 1, 0);

    *(volatile s32 *)0x80000000 = 1;
}
