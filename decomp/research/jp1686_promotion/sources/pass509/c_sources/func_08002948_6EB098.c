#include "m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08002998_6EB0E8();                     /* static */

void func_08002948_6EB098(void *arg0, void *arg1) {
    M2C_FIELD(arg1, u16 *, 0x16) = (u16) ((M2C_FIELD(arg1, u16 *, 0x16) + 0x40) & 0x3FF);
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x14;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08002998_6EB0E8);
    }
}
