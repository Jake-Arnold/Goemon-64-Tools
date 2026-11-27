#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
extern char func_8021BB04_5D6FD4;
extern M2C_UNK func_08001324_6C0A74;

void func_080012B8_6C0A08(void *arg0, M2C_UNK arg1) {
    if (((s32  (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8021BB04_5D6FD4)(arg0, 0xC3520000, 0x41B00000, 0x3F000000) == 0) {
        ((M2C_UNK (*)(M2C_UNK))&func_80038B98_39798)(0x155);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x14;
        ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08001324_6C0A74);
    }

    *(volatile s32 *)0x80000000 = 1;
}
