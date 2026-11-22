#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(s32, void *);           /* extern */

void func_8022792C_5E2EBC(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, s32 *, 0x68);
    if (!(temp_v0 & 0x20)) {
        if (temp_v0 & 0x40) {
            func_80034E8C_35A8C(M2C_FIELD(arg0, s32 *, 0xBC), arg0);
            return;
        }
        M2C_FIELD(arg0, f32 *, 0x7C) = (f32) M2C_FIELD(arg0, f32 *, 0xC0);
    }
}
