#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
extern M2C_UNK func_08005684_6C4DD4;

void func_08005624_6C4D74(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 1);
        ((M2C_UNK(*)())&func_80038B98_39798)(0x124);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08005684_6C4DD4);
    }
}
