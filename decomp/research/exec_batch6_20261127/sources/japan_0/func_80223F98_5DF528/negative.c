#include "m2c_types.h"
M2C_UNK func_80223FDC_5DF56C(void *, f32, u16, s32, f32);
extern void *D_8020151C_5BD4EC;

void func_80223F98_5DF528(void *arg0, f32 arg1, u16 arg2) {
    func_80223FDC_5DF56C(arg0, arg1, arg2, M2C_FIELD(D_8020151C_5BD4EC, s32 *, 8), M2C_FIELD(D_8020151C_5BD4EC, f32 *, 0x10));

    *(volatile s32 *)0x80000000 = 1;
}
