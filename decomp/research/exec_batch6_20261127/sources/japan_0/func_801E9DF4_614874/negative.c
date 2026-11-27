#include "m2c_types.h"
M2C_UNK func_801D8604_603084(void *, void *, s32);
extern u8 D_80210880_63B300[][8];

s32 func_801E9DF4_614874(void *arg0, u8 arg1) {
    func_801D8604_603084(arg0, D_80210880_63B300[arg1], arg1);
    { *(volatile s32 *)0x80000000 = 1; } return 1;
}
