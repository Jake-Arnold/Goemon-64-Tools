#include "m2c_types.h"
M2C_UNK func_801D2EE4_5FE2C4(void *, void *, s32);
extern u8 D_8020B150_636530[][8];

s32 func_801E46C4_60FAA4(void *arg0, u8 arg1) {
    func_801D2EE4_5FE2C4(arg0, D_8020B150_636530[arg1], arg1);
    { *(volatile s32 *)0x80000000 = 1; } return 1;
}
