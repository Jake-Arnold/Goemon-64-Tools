#include "m2c_types.h"
M2C_UNK func_80034B44_35744(void);
M2C_UNK func_8021CDBC_5D834C(void *, s32);

void func_080006D4_6F8264(void *arg0, M2C_UNK arg1) {
    M2C_UNK (*fn1)(void *, s32) = func_8021CDBC_5D834C;
    M2C_UNK (*fn2)(void) = func_80034B44_35744;
    void *temp_v0;

    fn1(arg0, 0);
    temp_v0 = M2C_FIELD(arg0, void **, 0xDC);
    if (temp_v0 != NULL) {
        M2C_FIELD(temp_v0, s8 *, 0xD0) = 1;
    }
    fn2();
}
