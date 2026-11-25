#include "m2c_types.h"
extern char func_8003521C_35E1C;
M2C_UNK func_08001974_6C10C4();                     /* static */

void func_08001920_6C1070(void *arg0, void *arg1) {
    if (!(M2C_FIELD(arg1, f32 *, 0xC) < -10.0f)) {
        M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
        M2C_FIELD(arg1, f32 *, 0xC) = -10.0f;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08001974_6C10C4);
    }
}
