#include "m2c_types.h"
extern M2C_UNK func_8003521C_35E1C;
extern M2C_UNK func_0800266C_723C8C;

void func_08002618_723C38(s32 arg0, void *arg1) {
    M2C_FIELD(arg1, u16 *, 0x14) = (M2C_FIELD(arg1, u16 *, 0x14) + 8) & 0x3FF;
    if (M2C_FIELD(arg1, u16 *, 0x14) >= 0x46) {
        M2C_FIELD(arg1, u16 *, 0x14) = 0x46;
        ((void (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_0800266C_723C8C);
    }
}
