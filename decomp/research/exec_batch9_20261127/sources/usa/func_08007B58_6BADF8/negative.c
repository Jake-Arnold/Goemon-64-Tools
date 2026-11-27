#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
M2C_UNK func_80218D7C_5D424C(void *, M2C_UNK, M2C_UNK, M2C_UNK);
extern M2C_UNK func_08007BB0_6BAE50;

void func_08007B58_6BADF8(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, u16 *, 0x8A)--) {
        return;
    }
    ((void (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))func_80218D7C_5D424C)(arg0, 0xA, 0x50, 0);
    ((void (*)(M2C_UNK *))func_8003521C_35E1C)(&func_08007BB0_6BAE50);

    *(volatile s32 *)0x80000000 = 1;
}
