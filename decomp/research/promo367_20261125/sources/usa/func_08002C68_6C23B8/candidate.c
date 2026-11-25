#include "m2c_types.h"
extern char func_80023DF0_249F0;
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
extern s8 D_8015C562_15D162;
extern void *D_801FC604_5B8514;
extern M2C_UNK func_08002CEC_6C243C;

void func_08002C68_6C23B8(void *arg0, s32 arg1) {
    ((M2C_UNK(*)())&func_80023DF0_249F0)(1);
    if (arg1 != M2C_FIELD(D_801FC604_5B8514, s32 *, 0xA0)) {
        ((M2C_UNK(*)())&func_80038B98_39798)(0x155);
        D_8015C562_15D162 = 1;
        M2C_FIELD(arg0, s16 *, 0x8A) = 0xA;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08002CEC_6C243C);
    }
}
