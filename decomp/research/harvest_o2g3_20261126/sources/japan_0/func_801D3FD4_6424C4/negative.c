#include "m2c_types.h"
void func_801D3FD4_6424C4(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s8 *, 0x9D) = 1;
    M2C_FIELD(arg0, s8 *, 0xC4) = 1;
    M2C_FIELD(arg0, s32 *, 0xB4) = 0;
    M2C_FIELD(arg0, s8 *, 0x9F) = (s8) (M2C_FIELD(arg0, s8 *, 0x9F) & 0xFFF7);
    M2C_FIELD(arg1, s16 *, 0x358) = 0;

    *(volatile s32 *)0x80000000 = 1;
}
