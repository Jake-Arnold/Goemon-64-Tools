#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D8738_6031B8(void *, M2C_UNK);      /* extern */
M2C_UNK func_801D9238_603CB8(void *, f32, M2C_UNK); /* extern */
M2C_UNK func_801D9620_6040A0(void *, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801DBC28_6066A8(void *, M2C_UNK);      /* extern */
M2C_UNK func_801F7E10_622890();                     /* static */

void func_801F7D74_6227F4(void *arg0, void *arg1) {
    func_801D8738_6031B8(arg1, 0x42200000);
    func_801D9238_603CB8(arg0, M2C_FIELD(arg1, f32 *, 0x20) * 300.0f, 0x10);
    func_801D9620_6040A0(arg0, 0, 8);
    func_801DBC28_6066A8(arg0, 0xBE4CCCCD);
    if (M2C_FIELD(arg0, f32 *, 0x74) <= 0.0f) {
        func_80034E8C_35A8C(func_801F7E10_622890);
    }
}
