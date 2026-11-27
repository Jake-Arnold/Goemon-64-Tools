#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
M2C_UNK func_8021664C_5D1B1C(void *, M2C_UNK, M2C_UNK, M2C_UNK);
extern M2C_UNK func_08002FA4_6B6244;

void func_08002F50_6B61F0(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((void (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))func_8021664C_5D1B1C)(arg0, 3, 0x3EAAAAAB, 0);
        ((void (*)(M2C_UNK *))func_8003521C_35E1C)(&func_08002FA4_6B6244);
    }
}
