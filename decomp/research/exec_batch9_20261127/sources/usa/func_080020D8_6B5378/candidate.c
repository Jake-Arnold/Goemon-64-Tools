#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
M2C_UNK func_80218D7C_5D424C(void *, M2C_UNK, M2C_UNK, M2C_UNK);
extern s8 D_8015CDB6;
extern M2C_UNK func_08002128_6B53C8;

void func_080020D8_6B5378(void *arg0, M2C_UNK arg1) {
    D_8015CDB6 = 0;
    ((void (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))func_80218D7C_5D424C)(arg0, 0x190, 0x190, 0xC8);
    ((void (*)(M2C_UNK *))func_8003521C_35E1C)(&func_08002128_6B53C8);
}
