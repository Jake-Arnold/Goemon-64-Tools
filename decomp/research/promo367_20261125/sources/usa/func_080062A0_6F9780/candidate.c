#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
M2C_UNK func_08006318_6F97F8();                     /* static */
extern M2C_UNK D_8015CC30_15D830;

void func_080062A0_6F9780(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, u16 *, 0xDA) != 0) {
        M2C_FIELD(&D_8015CC30_15D830, s32 *, 0xD4) = (s32) (M2C_FIELD(&D_8015CC30_15D830, s32 *, 0xD4) | 1);
        ((M2C_UNK(*)())&func_80038B98_39798)(0x224, arg0);
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 1);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08006318_6F97F8, arg0);
    }
}
