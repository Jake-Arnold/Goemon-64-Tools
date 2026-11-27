#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_80218DCC_5D429C;
extern char func_8021C628_5D7AF8;
extern M2C_UNK func_08002070_6DBF40;

void func_08001FDC_6DBEAC(void *arg0, M2C_UNK arg1) {
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        ((M2C_UNK  (*)(void *, M2C_UNK))&func_8021C628_5D7AF8)(arg0, 0x40000000);
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & 0xFEFFFFFF);
        ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8021664C_5D1B1C)(arg0, 4, 0x3E800000, 4);
        ((M2C_UNK (*)(void *, M2C_UNK))&func_80218DCC_5D429C)(arg0, 5);
        ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08002070_6DBF40);
    }

    *(volatile s32 *)0x80000000 = 1;
}
