#include "m2c_types.h"
extern char func_80219E70_5D5340;
extern char func_8021C654_5D7B24;
extern char func_80226840_5E1D10;

void func_08000000_71BA80(void *arg0) {
    M2C_FIELD(arg0, s32 *, 0x60) = 0x12800F21;
    M2C_FIELD(arg0, s32 *, 0x64) = 0x20;
    ((M2C_UNK  (*)(void *, u16))&func_80226840_5E1D10)(arg0, M2C_FIELD(arg0, u16 *, 0xD2));
    ((M2C_UNK (*)(void *))&func_8021C654_5D7B24)(arg0);
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK))&func_80219E70_5D5340)(arg0, 5, 0);

    *(volatile s32 *)0x80000000 = 1;
}
