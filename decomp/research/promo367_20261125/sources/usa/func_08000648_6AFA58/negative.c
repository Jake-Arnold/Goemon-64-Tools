#include "../m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
extern char func_80221C0C_5DD0DC;
M2C_UNK func_080004FC_6AF90C(s32, M2C_UNK);         /* static */
M2C_UNK func_08000620_6AFA30();                     /* static */

void func_08000648_6AFA58(s32 arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    ((M2C_UNK(*)())&func_80038B98_39798)(0x34F);
    func_080004FC_6AF90C(arg0, 0x12800761);
    ((M2C_UNK(*)())&func_80221C0C_5DD0DC)(arg0, 0, 0x3E800000, 1);
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08000620_6AFA30);
}
