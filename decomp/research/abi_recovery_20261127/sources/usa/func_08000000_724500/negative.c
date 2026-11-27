#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80218D7C_5D424C;
extern M2C_UNK func_08000064_724564;

void func_08000000_724500(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x64) = (s32) (M2C_FIELD(arg0, s32 *, 0x64) | 0x800002);
    M2C_FIELD(arg0, s8 *, 0xDC) = 5;
    ((M2C_UNK  (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_80218D7C_5D424C)(arg0, 0, 0, 0);
    ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08000064_724564);

    *(volatile s32 *)0x80000000 = 1;
}
