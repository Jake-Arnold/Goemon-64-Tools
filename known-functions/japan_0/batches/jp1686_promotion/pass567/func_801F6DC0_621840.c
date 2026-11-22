#include "../m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D88EC_60336C(void *, M2C_UNK *);    /* extern */
M2C_UNK func_801F6180_620C00();                     /* static */
M2C_UNK func_801FCE00_627880();                     /* static */
extern M2C_UNK D_802109A0_63B420;

void func_801F6DC0_621840(void *arg0, M2C_UNK arg1) {
    func_801FCE00_627880();
    func_801D88EC_60336C(arg0, &D_802109A0_63B420);
    M2C_FIELD(arg0, f32 *, 0x74) = 1.0f;
    func_80034E8C_35A8C(func_801F6180_620C00);
}
