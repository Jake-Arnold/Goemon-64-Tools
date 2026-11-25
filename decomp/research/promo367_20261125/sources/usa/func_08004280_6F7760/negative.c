#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
extern u8 D_8015CD68;
extern M2C_UNK func_080042F4_6F77D4;

void func_08004280_6F7760(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if ((s32) D_8015CD68 >= 6) {
        ((M2C_UNK(*)())&func_80038B98_39798)(0x15E, arg0);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x78;
        M2C_FIELD(arg0, f32 *, 0x7C) = -0.5f;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_080042F4_6F77D4, arg0);
    }
}
