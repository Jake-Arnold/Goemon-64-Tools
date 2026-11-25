#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
extern M2C_UNK func_080038B8_6B6B58;

void func_08003850_6B6AF0(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        ((M2C_UNK(*)())&func_80038B98_39798)(0x10A, arg0);
        M2C_FIELD(arg0, u16 *, 0x8A) = 0x1EU;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_080038B8_6B6B58, arg0);
    }
}
