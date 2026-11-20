#include "../m2c_types.h"
M2C_UNK func_801ED278_5A9248();                     /* extern */

void func_801FBECC_5B7E9C(void *arg0) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x5C);
    M2C_FIELD(arg0, s8 *, 0x61) = 1;
    M2C_FIELD(temp_v0, f32 *, 0x50) = (f32) (M2C_FIELD(temp_v0, f32 *, 0x48) * -1.0f);
    M2C_FIELD(arg0, s16 *, 0x40) = 0;
    M2C_FIELD(arg0, u8 *, 0x30) = (u8) (M2C_FIELD(arg0, u8 *, 0x30) | 1);
    func_801ED278_5A9248();
}
