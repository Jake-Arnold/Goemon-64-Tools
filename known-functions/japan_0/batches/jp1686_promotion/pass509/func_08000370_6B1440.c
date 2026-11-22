#include "m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_080003C0_6B1490();                     /* static */

void func_08000370_6B1440(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, s32 *, 0x68) & 0x20) {
        M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080003C0_6B1490);
    }
}
