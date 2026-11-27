#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);
M2C_UNK func_8021B3BC_5D694C(void *, M2C_UNK, M2C_UNK, M2C_UNK);
extern M2C_UNK func_08002F40_6BACC0;

void func_08002EEC_6BAC6C(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((void (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))func_8021B3BC_5D694C)(arg0, 3, 0x3EAAAAAB, 0);
        ((void (*)(M2C_UNK *))func_80034E8C_35A8C)(&func_08002F40_6BACC0);
    }
}
