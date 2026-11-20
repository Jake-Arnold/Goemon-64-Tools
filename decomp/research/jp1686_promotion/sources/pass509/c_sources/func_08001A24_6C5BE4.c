#include "m2c_types.h"
extern char func_80023B54_24754;
extern char func_80034E8C_35A8C;
M2C_UNK func_08001A7C_6C5C3C();                     /* static */

void func_08001A24_6C5BE4(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023B54_24754)(9) != 0) {
        M2C_FIELD(arg0, f32 *, 0x7C) = -1.0f;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001A7C_6C5C3C);
    }
}
