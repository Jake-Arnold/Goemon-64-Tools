#include "m2c_types.h"
s32 func_801E8C44_5A4B54(void *, u8);

s32 func_801F0CE4_5ACBF4(void *arg0) {
    { *(volatile int *)0x80000000 = 1; } return (func_801E8C44_5A4B54(M2C_FIELD(arg0, void **, 0x84), 0x1D) != 0) ||
           (func_801E8C44_5A4B54(M2C_FIELD(arg0, void **, 0x84), 0x1E) != 0) ||
           (func_801E8C44_5A4B54(M2C_FIELD(arg0, void **, 0x84), 0x1F) != 0);
}
