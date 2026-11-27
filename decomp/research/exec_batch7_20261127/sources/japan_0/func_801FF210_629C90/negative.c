#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);
extern f64 D_80213FE0_63EA60;
extern void *D_80214600_63F080;
extern M2C_UNK func_801FF2A4_629D24;

void func_801FF210_629C90(void *arg0, M2C_UNK arg1) {
    f32 *temp = &M2C_FIELD(D_80214600_63F080, f32 *, 0xA0);
    *temp = (f32) ((f64) *temp - D_80213FE0_63EA60);
    if (*temp <= -80.0f) {
        *temp = -80.0f;
        M2C_FIELD(D_80214600_63F080, s8 *, 0x2C1) = 5;
        M2C_FIELD(arg0, s32 *, 0x7C) = 0xA0;
        M2C_FIELD(arg0, s32 *, 0x80) = 0x32;
        func_80034E8C_35A8C(&func_801FF2A4_629D24);
    }

    *(volatile s32 *)0x80000000 = 1;
}
