#include "../m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801F6EB8_621938();                     /* static */
M2C_UNK func_801FC74C_6271CC();                     /* static */
M2C_UNK func_801FC7A4_627224(void *);               /* static */

void func_801F6E68_6218E8(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x74) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x78) = -10.0f;
    func_801FC74C_6271CC();
    func_801FC7A4_627224(arg0);
    func_80034E8C_35A8C(func_801F6EB8_621938);
}
