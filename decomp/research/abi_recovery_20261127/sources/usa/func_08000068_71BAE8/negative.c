#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80226840_5E1D10;
extern M2C_UNK func_080000C0_71BB40;

void func_08000068_71BAE8(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x2C2;
    ((M2C_UNK  (*)(void *, u16))&func_80226840_5E1D10)(arg0, M2C_FIELD(arg0, u16 *, 0xD2));
    M2C_FIELD(arg0, s32 *, 0x60) = 0x221;
    ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_080000C0_71BB40);

    *(volatile s32 *)0x80000000 = 1;
}
