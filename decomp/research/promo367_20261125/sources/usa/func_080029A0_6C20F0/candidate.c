#include "m2c_types.h"
extern char func_80023DF0_249F0;
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
extern s8 D_8015C562_15D162;
extern void *D_801FC604_5B8514;
extern M2C_UNK func_08002A20_6C2170;

void func_080029A0_6C20F0(void *arg0, s32 arg1) {
    ((M2C_UNK(*)())&func_80023DF0_249F0)(0);
    if (arg1 != M2C_FIELD(D_801FC604_5B8514, s32 *, 0xA0)) {
        ((M2C_UNK(*)())&func_80038B98_39798)(0x155);
        D_8015C562_15D162 = 0;
        M2C_FIELD(arg0, s16 *, 0x8A) = 0xA;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08002A20_6C2170);
    }
}
