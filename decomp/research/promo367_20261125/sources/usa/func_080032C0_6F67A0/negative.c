#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
extern u8 D_8015CD68;
extern M2C_UNK func_0800333C_6F681C;

void func_080032C0_6F67A0(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if ((M2C_FIELD(arg0, u8 *, 0xD1) == 0) && ((s32) M2C_FIELD(arg0, u8 *, 0xD2) < (s32) D_8015CD68)) {
        ((M2C_UNK(*)())&func_80038B98_39798)(0x224, arg0);
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 1);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_0800333C_6F681C, arg0);
    }
}
