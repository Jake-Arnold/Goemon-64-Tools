#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
extern char func_80219E08_5D52D8;
extern char func_80221C0C_5DD0DC;
M2C_UNK func_08000F88_6B0398(s32, M2C_UNK (*)());   /* static */
M2C_UNK func_0800105C_6B046C();                     /* static */
M2C_UNK func_08001B5C_6B0F6C();                     /* static */

void func_08001128_6B0538(s32 arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    ((M2C_UNK(*)())&func_80038B98_39798)(0x353);
    func_08000F88_6B0398(arg0, func_08001B5C_6B0F6C);
    ((M2C_UNK(*)())&func_80221C0C_5DD0DC)(arg0, 0, 0x3E800000, 1);
    ((M2C_UNK(*)())&func_80219E08_5D52D8)(arg0, 0x3FA00000);
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_0800105C_6B046C);
}
