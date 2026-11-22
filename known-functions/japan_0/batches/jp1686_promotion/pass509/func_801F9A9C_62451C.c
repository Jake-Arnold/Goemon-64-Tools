#include "m2c_types.h"
f32 func_8000EAC0_F6C0(s32, s32);                   /* extern */
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801DB8BC_60633C();                     /* extern */
M2C_UNK func_801F9B00_624580();                     /* static */
M2C_UNK func_801FCE00_627880(s32);                  /* static */
extern void *D_80214600_63F080;

void func_801F9A9C_62451C(s32 arg0, M2C_UNK arg1) {
    func_801DB8BC_60633C();
    func_801FCE00_627880(arg0);
    if (func_8000EAC0_F6C0(arg0, M2C_FIELD(D_80214600_63F080, s32 *, 0x1CC)) <= 180.0f) {
        func_80034E8C_35A8C(func_801F9B00_624580);
    }
}
