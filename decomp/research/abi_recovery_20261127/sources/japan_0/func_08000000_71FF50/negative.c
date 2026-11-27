#include "m2c_types.h"
extern char func_8021EBE0_5DA170;
extern char func_802213C4_5DC954;
extern char func_8022B5B0_5E6B40;

void func_08000000_71FF50(void *arg0) {
    M2C_FIELD(arg0, s32 *, 0x60) = 0x12800F21;
    M2C_FIELD(arg0, s32 *, 0x64) = 0x20;
    ((M2C_UNK  (*)(void *, u16))&func_8022B5B0_5E6B40)(arg0, M2C_FIELD(arg0, u16 *, 0xD2));
    ((M2C_UNK (*)(void *))&func_802213C4_5DC954)(arg0);
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK))&func_8021EBE0_5DA170)(arg0, 5, 0);

    *(volatile s32 *)0x80000000 = 1;
}
