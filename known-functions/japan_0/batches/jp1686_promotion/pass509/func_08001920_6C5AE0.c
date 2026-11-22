#include "m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08001974_6C5B34();                     /* static */

void func_08001920_6C5AE0(void *arg0, void *arg1) {
    if (!(M2C_FIELD(arg1, f32 *, 0xC) < -10.0f)) {
        M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
        M2C_FIELD(arg1, f32 *, 0xC) = -10.0f;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001974_6C5B34);
    }
}
