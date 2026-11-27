#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
M2C_UNK func_8021664C_5D1B1C(void *, M2C_UNK, M2C_UNK, M2C_UNK);
extern M2C_UNK func_080018D0_6D09B0;

void func_08001884_6D0964(void *arg0, M2C_UNK arg1) {
    void (*fn1)(void *, M2C_UNK, M2C_UNK, M2C_UNK) = (void (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))func_8021664C_5D1B1C;
    void (*fn2)(M2C_UNK *) = (void (*)(M2C_UNK *))func_8003521C_35E1C;
    fn1(arg0, 0, 0x3EAAAAAB, 1);
    fn2(&func_080018D0_6D09B0);
}
