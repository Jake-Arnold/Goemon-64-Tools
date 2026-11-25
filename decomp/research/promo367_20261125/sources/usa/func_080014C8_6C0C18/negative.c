#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
M2C_UNK func_0800152C_6C0C7C();                     /* static */
extern f32 D_080089C0_6C8110;

void func_080014C8_6C0C18(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    ((M2C_UNK(*)())&func_80038B98_39798)(0x154);
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        M2C_FIELD(arg0, f32 *, 0x7C) = (f32) D_080089C0_6C8110;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_0800152C_6C0C7C);
    }
}
