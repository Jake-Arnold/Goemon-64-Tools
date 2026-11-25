#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80038BC8_397C8;
extern M2C_UNK func_08000DC4_713D34;

void func_08000D60_713CD0(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        ((M2C_UNK(*)())&func_80038BC8_397C8)(M2C_FIELD(arg0, u16 *, 0xD8), arg0);
        M2C_FIELD(arg0, u16 *, 0x8A) = 0U;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08000DC4_713D34, arg0);
    }
}
