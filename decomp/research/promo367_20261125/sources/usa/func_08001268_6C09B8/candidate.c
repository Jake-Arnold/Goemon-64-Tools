#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
extern M2C_UNK func_080012B8_6C0A08;

void func_08001268_6C09B8(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        ((M2C_UNK(*)())&func_80038B98_39798)(0x154);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_080012B8_6C0A08);
    }
}
