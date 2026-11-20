#include "m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08003384_6FAF14();                     /* static */

void func_08003338_6FAEC8(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & ~1);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08003384_6FAF14);
    }
}
