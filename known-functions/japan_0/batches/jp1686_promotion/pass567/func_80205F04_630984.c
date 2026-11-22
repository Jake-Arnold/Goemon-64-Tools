#include "../m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_80205F48_6309C8();                     /* static */

void func_80205F04_630984(void *arg0, void *arg1) {
    func_80034E8C_35A8C(func_80205F48_6309C8);
    M2C_FIELD(arg0, f32 *, 0x90) = (f32) M2C_FIELD(arg1, f32 *, 8);
    M2C_FIELD(arg0, f32 *, 0x94) = (f32) M2C_FIELD(arg1, f32 *, 0x10);
}
