#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021DAEC_5D907C;
extern M2C_UNK func_08001CF0_6B9A70;

void func_08002F40_6BACC0(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x68) = (s32) (M2C_FIELD(arg0, s32 *, 0x68) & ~1);
    ((M2C_UNK  (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8021DAEC_5D907C)(arg0, 0, 0, 0);
    ((M2C_UNK (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_08001CF0_6B9A70);

    *(volatile s32 *)0x80000000 = 1;
}
