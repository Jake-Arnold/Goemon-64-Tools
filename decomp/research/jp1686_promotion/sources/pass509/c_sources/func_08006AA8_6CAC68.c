#include "m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08006B00_6CACC0();                     /* static */

void func_08006AA8_6CAC68(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, f32 *, 0x10) == 396.0f) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x3C;
        M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08006B00_6CACC0);
    }
}
