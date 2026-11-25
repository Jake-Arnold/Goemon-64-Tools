#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
extern char func_80219E08_5D52D8;
extern char func_80221C0C_5DD0DC;
M2C_UNK func_08000F88_6B0398(s32, M2C_UNK (*)());   /* static */
M2C_UNK func_0800105C_6B046C();                     /* static */
M2C_UNK func_08001A54_6B0E64();                     /* static */

void func_080010A4_6B04B4(s32 arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_80038B98_39798)(0x352);
    func_08000F88_6B0398(arg0, func_08001A54_6B0E64);
    ((M2C_UNK(*)())&func_80221C0C_5DD0DC)(arg0, 0, 0x3E800000, 1);
    ((M2C_UNK(*)())&func_80219E08_5D52D8)(arg0, 0x3FA00000);
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_0800105C_6B046C);
}
