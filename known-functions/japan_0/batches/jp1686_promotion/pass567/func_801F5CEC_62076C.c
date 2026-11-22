#include "../m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D88EC_60336C(void *, M2C_UNK *);    /* extern */
M2C_UNK func_801F5D3C_6207BC();                     /* static */
M2C_UNK func_801FC7A4_627224();                     /* static */
extern M2C_UNK D_80210998_63B418;

void func_801F5CEC_62076C(void *arg0, M2C_UNK arg1) {
    func_801FC7A4_627224();
    func_801D88EC_60336C(arg0, &D_80210998_63B418);
    M2C_FIELD(arg0, f32 *, 0x74) = 1.0f;
    func_80034E8C_35A8C(func_801F5D3C_6207BC);
}
