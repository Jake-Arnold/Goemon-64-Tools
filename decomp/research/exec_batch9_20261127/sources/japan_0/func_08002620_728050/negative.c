#include "m2c_types.h"
extern M2C_UNK func_80034E8C_35A8C;
extern M2C_UNK func_08002674_7280A4;

void func_08002620_728050(s32 arg0, void *arg1) {
    M2C_FIELD(arg1, u16 *, 0x14) = (M2C_FIELD(arg1, u16 *, 0x14) + 8) & 0x3FF;
    if (M2C_FIELD(arg1, u16 *, 0x14) >= 0x46) {
        M2C_FIELD(arg1, u16 *, 0x14) = 0x46;
        ((void (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_08002674_7280A4);
    }

    *(volatile s32 *)0x80000000 = 1;
}
