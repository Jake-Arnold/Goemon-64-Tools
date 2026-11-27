#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80218D7C_5D424C;
extern s8 D_8015CDB6;
extern M2C_UNK func_080024F0_6B5790;

void func_080024A0_6B5740(M2C_UNK arg0, M2C_UNK arg1) {
    D_8015CDB6 = 0;
    ((M2C_UNK  (*)(M2C_UNK, M2C_UNK, M2C_UNK, M2C_UNK))&func_80218D7C_5D424C)(arg0, 0x190, 0x190, 0xC8);
    ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_080024F0_6B5790);

    *(volatile s32 *)0x80000000 = 1;
}
