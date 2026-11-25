#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
extern f32 D_08008A54_6C81A4;
extern M2C_UNK func_08005C34_6C5384;

void func_08005BC0_6C5310(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        if (M2C_FIELD(arg0, u8 *, 0xD4) == 0) {
            ((M2C_UNK(*)())&func_80038B98_39798)(0x256, arg0);
        }
        M2C_FIELD(arg0, f32 *, 0x7C) = (f32) D_08008A54_6C81A4;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08005C34_6C5384, arg0);
    }
}
