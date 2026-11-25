#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
extern char func_801FB240_5B7150;
extern char func_8022026C_5DB73C;
extern s8 D_8015C562_15D162;
extern M2C_UNK D_8015CC30_15D830;
extern M2C_UNK func_08004B14_6F7FF4;

void func_08004A74_6F7F54(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, u16 *, 0xDA) != 0) {
        M2C_FIELD(&D_8015CC30_15D830, s32 *, 0xD4) = (s32) (M2C_FIELD(&D_8015CC30_15D830, s32 *, 0xD4) | 1);
        ((M2C_UNK(*)())&func_80038B98_39798)(0x108);
        ((M2C_UNK(*)())&func_801FB240_5B7150)();
        D_8015C562_15D162 = 1;
        ((M2C_UNK(*)())&func_8022026C_5DB73C)(arg0, 0xFF, 0xFF, 0xFF);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08004B14_6F7FF4);
    }
}
