#include "m2c_types.h"
extern char func_8021B09C_5D656C;
extern char func_8021BB04_5D6FD4;

void func_080030F0_6DCFC0(void *arg0, M2C_UNK arg1) {
    if (((s32  (*)(void *, s32, s32, M2C_UNK))&func_8021BB04_5D6FD4)(arg0, M2C_FIELD(arg0, s32 *, 0xDC), M2C_FIELD(arg0, s32 *, 0xE0), 0x3FACCCCD) == 0) {
        ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK))&func_8021B09C_5D656C)(arg0, 0, 1);
    }

    *(volatile s32 *)0x80000000 = 1;
}
