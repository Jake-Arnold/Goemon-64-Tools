#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
extern char func_8003D310_3DF10;
extern char func_8003F1D8_3FDD8;
extern void *D_8015CD60;
extern void *D_801FC604_5B8514;
extern M2C_UNK func_08002304_6C1A54;

void func_0800221C_6C196C(s32 arg0, s32 arg1) {
volatile unsigned int goemon_negative_control = 1;

    f32 temp_f0;
    f32 temp_f0_2;

    if (arg1 == M2C_FIELD(D_801FC604_5B8514, s32 *, 0xA0)) {
        temp_f0 = M2C_FIELD(D_8015CD60, f32 *, 8);
        if ((temp_f0 > 60.0f) && (temp_f0 < 90.0f)) {
            temp_f0_2 = M2C_FIELD(D_8015CD60, f32 *, 0x10);
            if ((temp_f0_2 > -90.0f) && (temp_f0_2 < -65.0f) && (((s32(*)())&func_8003F1D8_3FDD8)() == 0)) {
                ((M2C_UNK(*)())&func_80038B98_39798)(0x2A5);
                ((M2C_UNK(*)())&func_8003D310_3DF10)(0xD5);
                ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08002304_6C1A54);
            }
        }
    }
}
