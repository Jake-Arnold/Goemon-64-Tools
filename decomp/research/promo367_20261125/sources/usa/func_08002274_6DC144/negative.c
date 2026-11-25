#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_80218DCC_5D429C;
extern char func_802192B4_5D4784;
extern u16 D_8015CC30_15D830;
extern M2C_UNK func_0800235C_6DC22C;

void func_08002274_6DC144(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    if (M2C_FIELD(arg0, u8 *, 0xD8) != 0) {
        ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, (void *)2, 0x3F000000, 4);
    } else {
        ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 2, 0x3E800000, 4);
    }
    ((M2C_UNK(*)())&func_80218DCC_5D429C)(arg0, 3);
    M2C_FIELD(arg1, f32 *, 0x28) = (f32) M2C_FIELD(arg0, f32 *, 0xD0);
    if (D_8015CC30_15D830 & 1) {
        M2C_FIELD(arg0, s16 *, 0xDA) = (s16) (((s32(*)())&func_802192B4_5D4784)(0xA) + 1);
    } else {
        M2C_FIELD(arg0, s16 *, 0xDA) = 0;
    }
    M2C_FIELD(arg0, s16 *, 0x8A) = 0;
    ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_0800235C_6DC22C);
}
