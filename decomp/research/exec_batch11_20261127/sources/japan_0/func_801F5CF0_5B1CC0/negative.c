#include "m2c_types.h"
s32 func_801EDD04_5A9CD4(void *, u8);

s32 func_801F5CF0_5B1CC0(void *arg0) {
    { *(volatile int *)0x80000000 = 1; } return (func_801EDD04_5A9CD4(M2C_FIELD(arg0, void **, 0x84), 0x1D) != 0) ||
           (func_801EDD04_5A9CD4(M2C_FIELD(arg0, void **, 0x84), 0x1E) != 0) ||
           (func_801EDD04_5A9CD4(M2C_FIELD(arg0, void **, 0x84), 0x1F) != 0);
}
