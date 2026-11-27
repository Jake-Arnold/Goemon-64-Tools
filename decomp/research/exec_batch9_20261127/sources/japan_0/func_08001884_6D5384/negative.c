#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);
M2C_UNK func_8021B3BC_5D694C(void *, M2C_UNK, M2C_UNK, M2C_UNK);
extern M2C_UNK func_080018D0_6D53D0;

void func_08001884_6D5384(void *arg0, M2C_UNK arg1) {
    void (*fn1)(void *, M2C_UNK, M2C_UNK, M2C_UNK) = (void (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))func_8021B3BC_5D694C;
    void (*fn2)(M2C_UNK *) = (void (*)(M2C_UNK *))func_80034E8C_35A8C;
    fn1(arg0, 0, 0x3EAAAAAB, 1);
    fn2(&func_080018D0_6D53D0);

    *(volatile s32 *)0x80000000 = 1;
}
