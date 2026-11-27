#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);
M2C_UNK func_8021DAEC_5D907C(void *, M2C_UNK, M2C_UNK, M2C_UNK);
extern M2C_UNK func_08007B4C_6BF8CC;

void func_08007AF4_6BF874(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, u16 *, 0x8A)--) {
        return;
    }
    ((void (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))func_8021DAEC_5D907C)(arg0, 0xA, 0x50, 0);
    ((void (*)(M2C_UNK *))func_80034E8C_35A8C)(&func_08007B4C_6BF8CC);

    *(volatile s32 *)0x80000000 = 1;
}
