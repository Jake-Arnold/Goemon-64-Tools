#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
M2C_UNK func_08001594_6C5754();                     /* static */

void func_0800152C_6C56EC(void *arg0, void *arg1) {
    if (!(M2C_FIELD(arg1, f32 *, 0xC) > -35.0f)) {
        M2C_FIELD(arg1, f32 *, 0xC) = -35.0f;
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
        M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
        ((M2C_UNK(*)())&func_80038808_39408)(0x154);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001594_6C5754);
    }
}
