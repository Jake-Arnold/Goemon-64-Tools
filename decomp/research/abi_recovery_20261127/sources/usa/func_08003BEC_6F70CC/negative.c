#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
extern char func_8021B73C_5D6C0C;
extern M2C_UNK func_08003C54_6F7134;

void func_08003BEC_6F70CC(void *arg0, M2C_UNK arg1) {
    if (((s32  (*)(void *, M2C_UNK))&func_8021B73C_5D6C0C)(arg0, 0x42480000) != 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 1);
        ((M2C_UNK (*)(M2C_UNK))&func_80038B98_39798)(0x124);
        ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08003C54_6F7134);
    }

    *(volatile s32 *)0x80000000 = 1;
}
