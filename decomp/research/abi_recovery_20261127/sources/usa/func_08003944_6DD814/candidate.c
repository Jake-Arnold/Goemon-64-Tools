#include "m2c_types.h"
extern char func_08003C40_6DDB10;
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_80218DCC_5D429C;
extern M2C_UNK func_08003364_6DD234;

void func_08003944_6DD814(void *arg0, void *arg1) {
    ((M2C_UNK  (*)(void *))&func_08003C40_6DDB10)(arg0);
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        M2C_FIELD(arg0, s32 *, 0x68) = (s32) (M2C_FIELD(arg0, s32 *, 0x68) & ~1);
        ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8021664C_5D1B1C)(arg0, 0, 0x3E000000, 1);
        ((M2C_UNK (*)(void *, M2C_UNK))&func_80218DCC_5D429C)(arg0, 1);
        ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08003364_6DD234);
    }
}
